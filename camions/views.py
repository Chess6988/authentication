from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from .models import RubberTransport, Truck
from .forms import TruckForm

def register_truck(request):
    if request.method == 'POST':
        number_of_trucks = request.POST.get('number_of_trucks')
        if number_of_trucks:
            number_of_trucks = int(number_of_trucks)
            # Display success message
            messages.success(request, f'{number_of_trucks} trucks will be registered.')

            # Redirect to the truck information page
            return HttpResponseRedirect(reverse('register_truck_info') + f'?count={number_of_trucks}')
    
    return render(request, 'camions/register_truck.html')


# Define the missing register_truck_info view
def register_truck_info(request):
    count = int(request.GET.get('count', 1))  # Get the number of trucks from the URL parameter
    if request.method == 'POST':
        trucks = []
        for i in range(count):
            form = TruckForm(request.POST)
            if form.is_valid():
                truck = form.save()  # Save the truck instance
                trucks.append(truck)
            else:
                return render(request, 'camions/truck_information.html', {'form': form, 'count': count})

        # After all trucks are saved, create RubberTransport entries for each truck
        for truck in trucks:
            RubberTransport.objects.create(
                truck=truck,
                number_of_truck=1,  # You can modify this based on your logic
                tons_of_rubber=0.0, 
                price_per_ton=0.0  # You can set a default or get from form
            )
        
        # Redirect after saving truck details and RubberTransport entries
        return redirect('some_success_page')

    # Create empty forms for each truck
    forms = [TruckForm() for _ in range(count)]
    return render(request, 'camions/truck_information.html', {'forms': forms, 'count': count})
