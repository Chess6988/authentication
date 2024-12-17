import re
from django.shortcuts import render, redirect,  get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.urls import reverse
from .models import RubberTransport, Truck
from .forms import TruckForm, RubberTransportForm
from django.core.exceptions import ValidationError
from django.forms import formset_factory 
from django.db.models import Sum ,F, FloatField, Prefetch
from decimal import Decimal

# Added recently
from django.utils.timezone import now
from collections import defaultdict
from datetime import datetime
from django.db.models import Q

from django.views.decorators.csrf import csrf_protect  # Import csrf_protect
from django.middleware.csrf import get_token

@csrf_protect  # Ensure CSRF protection for this view et enregistre le nombre de camions

def register_truck(request):
    if request.method == 'POST':
        # Ensure CSRF token is being generated and validated
        csrf_token = get_token(request)
        number_of_trucks = request.POST.get('number_of_trucks')

        if number_of_trucks:
            try:
                number_of_trucks = int(number_of_trucks)

                # Store the number of trucks in the session
                request.session['number_of_trucks'] = number_of_trucks

                # Display success message
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    f'{number_of_trucks} trucks will be registered.',
                    extra_tags='register_truck'
                )

                # Redirect to the truck information page
                return HttpResponseRedirect(reverse('truck_information'))
            except ValueError:
                # Handle the case where the input is not a valid integer
                messages.error(request, "Please enter a valid number.")
    
    # If GET request or POST fails, re-render the form
    return render(request, 'camions/register_truck.html')



def truck_information(request):
    number_of_trucks = request.session.get('number_of_trucks', 0)
    print(f"Number of trucks in session: {number_of_trucks}")

    if not number_of_trucks:
        messages.error(request, "Please enter the number of trucks first.")
        return redirect('register_truck')

    TruckFormSet = formset_factory(TruckForm, extra=number_of_trucks)

    if request.method == 'POST':
        formset = TruckFormSet(request.POST)
        print("Received POST data:", request.POST)

        if formset.is_valid():
            recently_registered_trucks = []
            duplicate_errors = False

            for form in formset:
                if form.cleaned_data:
                    matriculation_number = form.cleaned_data['matriculation_number']
                    today = now().date()

                    duplicate_truck = Truck.objects.filter(
                        matriculation_number=matriculation_number,
                        created_at__date=today
                    ).exists()

                    if duplicate_truck:
                        form.add_error(
                            'matriculation_number',
                            f"The matriculation number '{matriculation_number}' has already been registered today."
                        )
                        duplicate_errors = True
                    else:
                        try:
                            truck = form.save(commit=False)
                            truck.save()
                            recently_registered_trucks.append({
                                "id": truck.id,  # Add truck ID
                                "matriculation_number": truck.matriculation_number,
                                "created_at": truck.created_at.strftime('%Y-%m-%d %H:%M:%S')
                            })
                            print(f"Saved truck: {truck.id} - {truck.matriculation_number}")
                        except IntegrityError:
                            form.add_error('matriculation_number', f"Error saving '{matriculation_number}'.")
                            duplicate_errors = True

            if duplicate_errors:
                messages.error(request, "Some matriculation numbers could not be registered.")
                return render(request, 'camions/truck_information.html', {'forms': formset})

            request.session['recently_registered_trucks'] = recently_registered_trucks
            print("Session recently registered trucks:", request.session['recently_registered_trucks'])
            messages.success(request, "Trucks successfully registered.")
            return redirect('list_registered_trucks')
        else:
            print("Formset errors:", formset.errors)
            messages.error(request, "Please fix the errors in the forms.")
    else:
        formset = TruckFormSet()
        print("Rendering truck information page...")

    return render(request, 'camions/truck_information.html', {'forms': formset})




# Listing list of trucks with their matricules

def list_registered_trucks(request):
    # Date range filter from the request
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Retrieve trucks registered in the current session
    recently_registered = request.session.get('recently_registered_trucks', [])
    print(f"Recently registered trucks: {recently_registered}")

    # Fetch trucks from the database that match the matriculation numbers
    matriculation_numbers = [truck['matriculation_number'] for truck in recently_registered]
    trucks = Truck.objects.filter(matriculation_number__in=matriculation_numbers)

    # Prefetch related rubber transports for efficiency
    trucks = trucks.prefetch_related(
        Prefetch(
            'rubber_transports', 
            queryset=RubberTransport.objects.all()
        )
    )

    # Apply date range filter if provided
    if start_date and end_date:
        trucks = trucks.filter(
            created_at__date__gte=start_date,
            created_at__date__lte=end_date
        )

    # Group trucks by their creation date
    grouped_trucks = defaultdict(list)
    for truck in trucks:
        if not truck.id:
            print(f"Skipping truck with missing ID: {truck}")
            continue  # Skip trucks with missing IDs

        # Calculate the total recette for this truck
        recette = sum(
            Decimal(rt.tons_of_rubber) * rt.price_per_ton for rt in truck.rubber_transports.all()
        )

        # Format date to 'YYYY-MM-DD' and include recette in the grouped data
        created_date = truck.created_at.strftime('%Y-%m-%d')
        grouped_trucks[created_date].append({
            "id": truck.id,
            "matriculation_number": truck.matriculation_number,
            "created_at": truck.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "recette": recette,
            "rubber_transport_id": truck.rubber_transports.first().id if truck.rubber_transports.exists() else None,
        })

    # Debug grouped trucks
    print("Grouped Trucks:", grouped_trucks)

    # Convert defaultdict to a regular dictionary for rendering
    grouped_trucks = dict(grouped_trucks)

    return render(
        request,
        'camions/registered_trucks.html',
        {
            'grouped_trucks': grouped_trucks,
            'start_date': start_date,
            'end_date': end_date,
        }
    )


# Concerned with inputting inputs for tons of rubber and price per ton
def add_rubber_transport(request, truck_id):
    truck = get_object_or_404(Truck, id=truck_id)

    if request.method == "GET":
        # Fetch existing rubber transport data
        rubber_transport = RubberTransport.objects.filter(truck=truck).first()
        
        # Calculate the recette dynamically
        recette = RubberTransport.objects.filter(truck=truck).aggregate(
            total_recette=Sum(F("tons_of_rubber") * F("price_per_ton"), output_field=FloatField())
        )["total_recette"] or 0

        return JsonResponse({
            "success": True,
            "tons_of_rubber": rubber_transport.tons_of_rubber if rubber_transport else "",
            "price_per_ton": rubber_transport.price_per_ton if rubber_transport else "",
            "recette": float(recette),  # Dynamically calculate recette
            "rubber_transport_id": rubber_transport.id if rubber_transport else None,
        })

    if request.method == "POST":
        try:
            # Get input values from the form
            tons_of_rubber = float(request.POST.get("tons_of_rubber", 0))
            price_per_ton = float(request.POST.get("price_per_ton", 0))

            # Validate inputs
            if tons_of_rubber <= 0 or price_per_ton <= 0:
                return JsonResponse({"success": False, "error": "Values must be greater than zero."}, status=400)

            # Create or update the rubber transport record
            rubber_transport, created = RubberTransport.objects.update_or_create(
                truck=truck,
                defaults={"tons_of_rubber": tons_of_rubber, "price_per_ton": price_per_ton}
            )

            # Dynamically calculate the total recette
            recette = RubberTransport.objects.filter(truck=truck).aggregate(
                total_recette=Sum(F("tons_of_rubber") * F("price_per_ton"), output_field=FloatField())
            )["total_recette"] or 0

            return JsonResponse({
                "success": True,
                "recette": float(recette),  # Send the updated recette value
                "rubber_transport_id": rubber_transport.id,
            })
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request method."}, status=405)




    
# Editing existing ton of rubber and price per ton
def edit_rubber_transport(request):
    if request.method == "POST":
        rubber_transport_id = request.POST.get("rubber_transport_id")
        rubber_transport = get_object_or_404(RubberTransport, id=rubber_transport_id)

        try:
            tons_of_rubber = float(request.POST.get("tons_of_rubber", 0.0))
            price_per_ton = float(request.POST.get("price_per_ton", 0.0))

            if tons_of_rubber <= 0 or price_per_ton <= 0:
                return JsonResponse({"success": False, "error": "Values must be greater than zero."})

            # Update rubber transport details
            rubber_transport.tons_of_rubber = tons_of_rubber
            rubber_transport.price_per_ton = price_per_ton
            rubber_transport.save()

            # Recalculate recette for the truck
            truck = rubber_transport.truck
            recette = RubberTransport.objects.filter(truck=truck).aggregate(
                total_recette=Sum(F('tons_of_rubber') * F('price_per_ton'), output_field=FloatField())
            )['total_recette'] or 0
            truck.recette = recette
            truck.save()

            return JsonResponse({"success": True, "recette": recette})
        except (ValueError, TypeError):
            return JsonResponse({"success": False, "error": "Invalid input."})

    return JsonResponse({"success": False, "error": "Invalid request."})
