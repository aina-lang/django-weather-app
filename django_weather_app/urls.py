from django.contrib import admin
from django.urls import path, re_path, include
from django.http import JsonResponse
from django.contrib.auth import views as auth_views

from weather import views

def health_check(request):
    """Simple health check endpoint for container health monitoring"""
    return JsonResponse({'status': 'healthy', 'service': 'django-weather-app'})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health_check'),
    
    # Auth URLs
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('accounts/register/', views.register, name='register'),
    
    # App URLs
    path('weather/', views.current_weather_view, name='current_weather'),
    path('', views.index, name='index'),
    
    # Catch-all for 404s
    re_path(r'^((?!admin|health|accounts|weather|static|media).)*$', views.custom_404, name='404'),
]

handler404 = views.custom_404
