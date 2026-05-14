# weather/views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from dotenv import load_dotenv
import os
import socket

from weather.utils.get_weather_with_uv import get_weather_with_uv
from weather.utils.get_weather_forecast import get_weather_forecast
from weather.utils import geo

# Load environment variables from .env file
load_dotenv()
openweathermap_api_key = os.getenv('OPENWEATHERMAP_API_KEY')

def get_server_info():
    """Helper to get pod and node information."""
    return {
        'pod_name': os.getenv('POD_NAME', 'local'),
        'node_name': os.getenv('NODE_NAME', 'local')
    }

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def weather_search(request):
    """API endpoint to search for weather or forecast."""
    city = request.GET.get('city', '').strip()
    option = request.GET.get('option', 'weather')

    if not city:
        detected_city = geo.index(request)
        if detected_city:
            city = detected_city
        else:
            return Response({'error': 'City is required'}, status=status.HTTP_400_BAD_REQUEST)

    server_info = get_server_info()

    if option == "weather":
        weather = get_weather_with_uv(openweathermap_api_key, city)
        if weather:
            return Response({
                'type': 'weather',
                'city': city,
                'data': weather,
                'server_info': server_info
            })
        return Response({'error': f"Could not retrieve weather for {city}"}, status=status.HTTP_404_NOT_FOUND)
    
    elif option == "forecast":
        forecast = get_weather_forecast(openweathermap_api_key, city)
        if forecast:
            return Response({
                'type': 'forecast',
                'city': city,
                'data': forecast,
                'server_info': server_info
            })
        return Response({'error': f"Could not retrieve forecast for {city}"}, status=status.HTTP_404_NOT_FOUND)

    return Response({'error': 'Invalid option'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """API endpoint for user registration."""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create(
        username=username,
        password=make_password(password)
    )
    return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """API health check."""
    return Response({
        'status': 'healthy',
        'server_info': get_server_info()
    })

from django.http import JsonResponse

def cluster_info(request):
    return JsonResponse({
        'pod_name': os.getenv('POD_NAME', 'local'),
        'node_name': os.getenv('NODE_NAME', 'local'),
        'status': 'ok'
    })