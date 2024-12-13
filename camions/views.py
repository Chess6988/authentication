import re
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from .models import RubberTransport, Truck
from .forms import TruckForm, RubberTransportForm
from django.core.exceptions import ValidationError
from django.forms import formset_factory 

# Added recently
from django.utils.timezone import now
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



# Define the view for truck matriculation
def truck_information(request):
    # Get the number of trucks from the session
    number_of_trucks = request.session.get('number_of_trucks', 0)
    print(f"Number of trucks in session: {number_of_trucks}")

    if not number_of_trucks:
        messages.error(request, "Please enter the number of trucks first.")
        return redirect('register_truck')

    # Create a formset with the specified number of trucks
    TruckFormSet = formset_factory(TruckForm, extra=number_of_trucks)

    if request.method == 'POST':
        formset = TruckFormSet(request.POST)
        print("Received POST data:", request.POST)  # Debug POST data

        if formset.is_valid():
            print("Formset is valid.")
            recently_registered_trucks = []  # Store matriculation numbers of newly added trucks
            duplicate_errors = False  # Track if there are any duplicates

            for form in formset:
                if form.cleaned_data:
                    matriculation_number = form.cleaned_data['matriculation_number']
                    today = now().date()  # Current day

                    # Check for duplicates registered today
                    duplicate_truck = Truck.objects.filter(
                        matriculation_number=matriculation_number,
                        created_at__date=today  # Filter by date only
                    ).exists()

                    if duplicate_truck:
                        # Add an error for the duplicate truck
                        form.add_error(
                            'matriculation_number',
                            f"The matriculation number '{matriculation_number}' has already been registered today."
                        )
                        duplicate_errors = True
                    else:
                        try:
                            # Save the truck if no duplicate exists
                            truck = form.save(commit=False)
                            truck.save()  # created_at is automatically added here
                            recently_registered_trucks.append({
                                "matriculation_number": truck.matriculation_number,
                                "created_at": truck.created_at.strftime('%Y-%m-%d %H:%M:%S')  # Save as string for session
                            })
                            print(f"Saved truck: {truck.matriculation_number}, created_at: {truck.created_at}")
                        except IntegrityError:
                            # Handle unexpected database integrity errors
                            form.add_error('matriculation_number', f"An unexpected error occurred while saving '{matriculation_number}'.")
                            duplicate_errors = True

            if duplicate_errors:
                messages.error(request, "Some matriculation numbers could not be registered. Please correct them.")
                return render(request, 'camions/truck_information.html', {'forms': formset})

            # Save the recently registered trucks in the session for display
            request.session['recently_registered_trucks'] = recently_registered_trucks
            messages.success(request, "Trucks successfully registered.")
            return redirect('list_registered_trucks')
        else:
            print("Formset is invalid.")
            print("Formset errors:", formset.errors)  # Debug formset errors
            messages.error(request, "Please fix the errors in the forms.")
    else:
        formset = TruckFormSet()
        print("Rendering truck information page...")

    return render(request, 'camions/truck_information.html', {'forms': formset})



def list_registered_trucks(request):
    # Retrieve trucks registered in the current session
    recently_registered = request.session.get('recently_registered_trucks', [])
    print(f"Recently registered trucks: {recently_registered}")

    # Fetch trucks from the database that match the matriculation numbers
    matriculation_numbers = [truck['matriculation_number'] for truck in recently_registered]
    trucks = Truck.objects.filter(matriculation_number__in=matriculation_numbers)

    # Pass trucks with created_at information to the template
    trucks_with_dates = [
        {
            "matriculation_number": truck.matriculation_number,
            "created_at": truck.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        for truck in trucks
    ]

    return render(request, 'camions/registered_trucks.html', {'registered_trucks': trucks_with_dates})
