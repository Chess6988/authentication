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
def truck_information_view(request):
    # Récupérer le nombre de camions depuis la session
    number_of_trucks = request.session.get('number_of_trucks', 1)  # Par défaut, 1 camion
    TruckFormSet = formset_factory(TruckForm, extra=number_of_trucks)

    if request.method == 'POST':
        formset = TruckFormSet(request.POST)
        if formset.is_valid():
            valid_trucks = []  # Stocker les matriculations valides
            invalid = False  # Indicateur pour savoir si une matriculation est invalide

            for form in formset:
                matriculation_number = form.cleaned_data.get('matriculation_number')
                if matriculation_number:
                    try:
                        # Valider et enregistrer le camion
                        truck = Truck(matriculation_number=matriculation_number)
                        truck.full_clean()  # Valider les données
                        truck.save()  # Sauvegarder dans la base de données
                        valid_trucks.append(truck.matriculation_number)  # Ajouter aux matriculations valides
                    except ValidationError:
                        invalid = True
                        messages.error(request, f"Le numéro de matriculation {matriculation_number} est invalide ou déjà utilisé.")
                        break

            if invalid:
                return render(request, 'camions/truck_information.html', {'forms': formset})

            # Sauvegarder les camions valides dans la session et rediriger
            request.session['valid_trucks'] = valid_trucks
            return redirect('truck_data_form')  # Rediriger vers la page qui affiche les matriculations

        else:
            # Afficher un message d'erreur si les formulaires ne sont pas valides
            messages.error(request, "Veuillez remplir correctement tous les formulaires.")
    else:
        formset = TruckFormSet()  # Générer un formset vierge

    return render(request, 'camions/truck_information.html', {'forms': formset})

def truck_data_form_view(request):
    # Get the list of valid matriculations stored in the session
    valid_trucks = request.session.get('valid_trucks', [])

    # Pass the list of trucks to the template
    return render(request, 'camions/truck_data_form.html', {'valid_trucks': valid_trucks})