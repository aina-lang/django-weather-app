# weather/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from dotenv import load_dotenv
import os

from weather.utils.get_weather_with_uv import get_weather_with_uv
from weather.utils.get_weather_forecast import get_weather_forecast
from weather.utils import geo

# Load environment variables from .env file
load_dotenv()
openweathermap_api_key = os.getenv('OPENWEATHERMAP_API_KEY')

@login_required
def index(request):
    """Front page where the user can search for weather or forecast."""
    error_message = None
    city = request.GET.get('city', '').strip()

    # If no city in URL, try to determine it based on IP address
    if not city:
        detected_city = geo.index(request)
        if detected_city:
            city = detected_city

    is_htmx = request.headers.get('HX-Request')

    if request.method == "GET" and 'city' in request.GET:
        option = request.GET.get('option')
        if option == "weather":
            weather = get_weather_with_uv(openweathermap_api_key, city)  # type: ignore
            if weather:
                template = 'partials/current_weather_content.html' if is_htmx else 'current_weather.html'
                return render(request, template, {'weather': weather, 'city': city})
            error_message = f"Désolé, les données météo pour {city.capitalize()} n'ont pas pu être récupérées."
        elif option == "forecast":
            forecast = get_weather_forecast(openweathermap_api_key, city)  # type: ignore
            if forecast:
                template = 'partials/forecast_content.html' if is_htmx else 'forecast.html'
                return render(request, template, {'forecast': forecast, 'city': city})
            error_message = f"Désolé, les prévisions pour {city.capitalize()} n'ont pas pu être récupérées."

    if is_htmx and error_message:
        return HttpResponse(f'<div class="error-message">{error_message}</div>', status=200)

    return render(request, 'index.html', {'error_message': error_message, 'city': city})

def register(request):
    """View for user registration."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def current_weather_view(request):
    """Display fetched weather for the city determined by GeoIP."""
    city = geo.index(request)

    if not city:
        return render(request, '404.html', {'error_message': 'Impossible de déterminer votre ville.'})

    weather = get_weather_with_uv(openweathermap_api_key, city)  # type: ignore
    if weather:
        return render(request, 'current_weather.html', {'weather': weather, 'city': city})
    return HttpResponse(f"Désolé, les données météo pour {city.capitalize()} n'ont pas pu être récupérées.")

def custom_404(request, exception=None):
    """Handle 404 errors with custom page."""
    return render(request, '404.html', {'error_message': 'Page non trouvée.'}, status=404)