from django.shortcuts import render, redirect
from .forms import FlightForm
from django.db.models import Avg
from .models import Flight
def home(request):
    return render(request, 'flights/home.html')

def register_flight(request):
    if request.method == 'POST':
        form = FlightForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_flights')
    else:
        form = FlightForm()
    return render(request, 'flights/register_flight.html', {'form': form})

def list_flights(request):
    flights = Flight.objects.all().order_by('price')
    return render(request, 'flights/list_flights.html', {'flights': flights})

def flight_stats(request):
    national_flights = Flight.objects.filter(type=Flight.NATIONAL).count()
    international_flights = Flight.objects.filter(type=Flight.INTERNATIONAL).count()
    national_avg_price = Flight.objects.filter(type=Flight.NATIONAL).aggregate(Avg('price'))['price__avg'] or 0

    return render(request, 'flights/flight_stats.html', {
        'national_count': national_flights,
        'international_count': international_flights,
        'national_avg_price': national_avg_price,
    })