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
            # Display success message
            messages.success(request, f'{number_of_trucks} trucks will be registered.')

            # Redirect to the truck information page
            return HttpResponseRedirect(reverse('register_truck_info') + f'?count={number_of_trucks}')
    
    return render(request, 'camions/register_truck.html')

# Define the view for truck matriculation
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

        # Redirect to the next page to enter the tons and price
        truck_ids = [truck.id for truck in trucks]
        return redirect(reverse('enter_truck_data') + f'?truck_ids={",".join(map(str, truck_ids))}')
    
    forms = [TruckForm() for _ in range(count)]
    return render(request, 'camions/truck_information.html', {'forms': forms, 'count': count})

# New view to enter the tons and price per ton
def enter_truck_data(request):
    truck_ids = request.GET.get('truck_ids').split(',')  # Get truck IDs from the URL
    trucks = Truck.objects.filter(id__in=truck_ids)  # Fetch the trucks by their IDs

    if request.method == 'POST':
        for truck in trucks:
            tons = request.POST.get(f'tons_of_rubber_{truck.id}')
            price = request.POST.get(f'price_per_ton_{truck.id}')

            # Validate and create RubberTransport entry for each truck
            if tons and price:
                RubberTransport.objects.create(
                    truck=truck,
                    tons_of_rubber=float(tons),
                    price_per_ton=float(price)
                )
        
        return redirect('some_success_page')  # Redirect after successful form submission

    # Display forms for each truck
    forms = {truck.id: RubberTransportForm() for truck in trucks}
    return render(request, 'camions/truck_data_form.html', {'trucks': trucks, 'forms': forms})
