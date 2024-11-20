import re
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from .models import RubberTransport, Truck
from .forms import TruckForm, RubberTransportForm
from django.core.exceptions import ValidationError
from django.forms import formset_factory 

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
    # Retrieve the number of trucks from the session
    number_of_trucks = request.session.get('number_of_trucks', 0)

    if not number_of_trucks:
        # Redirect back to register_truck if no number is found in the session
        messages.error(request, "Please enter the number of trucks first.")
        return redirect('register_truck')

    # Create a formset for TruckForm with the number of trucks specified
    TruckFormSet = formset_factory(TruckForm, extra=number_of_trucks)

    if request.method == 'POST':
        formset = TruckFormSet(request.POST)

        if formset.is_valid():
            # Save each valid form's data
            for form in formset:
                if form.cleaned_data:
                    truck = form.save()

                    # Optionally, create RubberTransport entries for these trucks
                    RubberTransport.objects.create(truck=truck, number_of_truck=1)

            # Clear the session data and show a success message
            del request.session['number_of_trucks']
            messages.success(request, "All trucks have been successfully registered.")
            return redirect('register_truck')  # Redirect to the registration page or a success page
        else:
            messages.error(request, "Please fix the errors in the forms.")
    else:
        formset = TruckFormSet()  # Generate empty forms for GET request

    return render(request, 'camions/truck_information.html', {'forms': formset})