from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from .models import RubberTransport, Truck
from .forms import TruckForm, RubberTransportForm

def register_truck(request):
    if request.method == 'POST':
        number_of_trucks = request.POST.get('number_of_trucks')
        if number_of_trucks:
            number_of_trucks = int(number_of_trucks)
            # Display success message with a custom tag for filtering
            messages.add_message(request, messages.SUCCESS, f'{number_of_trucks} trucks will be registered.', extra_tags='register_truck')

            # Redirect to the truck information page without the message
            return HttpResponseRedirect(reverse('register_truck_info') + f'?count={number_of_trucks}')
    
    return render(request, 'camions/register_truck.html')
# Define the view for truck matriculation
 

def register_truck_info(request):
    try:
        count = int(request.GET.get('count', 1))
        if count <= 0:
            return HttpResponseBadRequest("The count parameter must be a positive integer.")

    except ValueError:
        # If count is not a valid integer
        return HttpResponseBadRequest("Invalid count parameter. Please provide a valid integer.")

    if request.method == 'POST':
        try:
            # Creating forms for each truck
            forms = [TruckForm(request.POST, prefix=str(i)) for i in range(count)]
            all_valid = all(form.is_valid() for form in forms)

            if all_valid:
                trucks = []
                for form in forms:
                    try:
                        truck = form.save()
                        trucks.append(truck)
                    except ValidationError as e:
                        # If a validation error occurs while saving a truck
                        form.add_error(None, f"Error saving truck: {e}")
                        return render(request, 'camions/truck_information.html', {'forms': forms, 'count': count})
                    except Exception as e:
                        # Catch any other exception that may occur
                        form.add_error(None, f"An unexpected error occurred: {e}")
                        return render(request, 'camions/truck_information.html', {'forms': forms, 'count': count})
                
                # Redirection vers 'enter_truck_data' après un enregistrement réussi
                redirect(reverse('enter_truck_data') + f'?truck_ids={",".join(map(str, truck_ids))}')
  
 

            else:
                # If one or more forms are invalid, render the page with errors
                return render(request, 'camions/truck_information.html', {'forms': forms, 'count': count})
        
        except Exception as e:
            # Catch any unexpected error during form processing
            return render(request, 'camions/truck_information.html', {
                'forms': forms,
                'count': count,
                'error_message': f"An error occurred: {e}"
            })

    # If GET request, create empty forms
    forms = [TruckForm(prefix=str(i)) for i in range(count)]
    return render(request, 'camions/truck_information.html', {'forms': forms, 'count': count})

# New view to enter the tons and price per ton

def enter_truck_data(request):
    truck_ids = request.GET.get('truck_ids')
    if not truck_ids:
        return render(request, 'camions/truck_data_form.html', {'error_message': 'No truck IDs provided.'})
    
    truck_ids_list = truck_ids.split(',')
    try:
        trucks = Truck.objects.filter(id__in=truck_ids_list)
        if not trucks.exists():
            return render(request, 'camions/truck_data_form.html', {'error_message': 'No trucks found for the provided IDs.'})
    except ValueError:
        return render(request, 'camions/truck_data_form.html', {'error_message': 'Invalid truck IDs.'})
    
    return render(request, 'camions/truck_data_form.html', {'trucks': trucks})