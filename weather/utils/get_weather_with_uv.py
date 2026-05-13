from requests import get
from datetime import datetime
import pytz
from django.core.cache import cache
from weather.utils.get_current_uv_index import get_current_uv_index

def get_weather_with_uv(openweathermap_api_key: str, city: str):
    # Try to fetch from the cache
    cache_key = f'weather_{city}'
    weather = cache.get(cache_key)

    if weather:
        return weather  # If there is data in the cache, return it

    # If the data is not in the cache, fetch it from the API
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={openweathermap_api_key}&units=metric&lang=fr'

    try:
        response = get(url).json()
        lat = response['coord']['lat']
        lon = response['coord']['lon']
        uv_response = get_current_uv_index(openweathermap_api_key, lat, lon)

        # Get current date in the city's timezone
        current_time = datetime.now(pytz.utc)

        # Convert sunrise and sunset to hours only
        sunrise_time = datetime.fromtimestamp(response['sys']['sunrise'], pytz.utc).strftime("%H:%M")
        sunset_time = datetime.fromtimestamp(response['sys']['sunset'], pytz.utc).strftime("%H:%M")

        weather = {
            'city': response['name'],
            'date': current_time,
            'temperature': round(response['main']['temp']),
            'feels_like': round(response['main']['feels_like']),
            'temp_max': round(response['main']['temp_max']),
            'temp_min': round(response['main']['temp_min']),
            'description': response['weather'][0]['description'],
            'humidity': response['main']['humidity'],
            'wind_speed': round(response['wind']['speed']),
            'wind_direction': response['wind']['deg'],
            'sunrise': sunrise_time,
            'sunset': sunset_time,
            'icon': response['weather'][0]['icon'],
            'uv_index': uv_response,
            'cloudiness': response['clouds']['all'],
            'visibility': response.get('visibility', 'N/A'),
            'rain': response.get('rain', {}).get('1h', '0 mm'),
            'snow': response.get('snow', {}).get('1h', '0 mm')
        }

        # Save the result in the cache for 10 minutes (600 seconds)
        cache.set(cache_key, weather, timeout=600)

        return weather

    except Exception as e:
        return None
