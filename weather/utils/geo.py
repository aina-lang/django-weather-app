# weather/utils/geo.py

from functools import lru_cache
import os
from ipware import get_client_ip  # type: ignore
from django.contrib.gis.geoip2 import GeoIP2
from django_weather_app import settings

@lru_cache
def _geoip():
    """Return a cached GeoIP2 instance using the configured GEOIP_PATH."""
    return GeoIP2(settings.GEOIP_PATH)

def get_client_ip_address(request):
    """
    Return client IP or None.

    Uses django-ipware so it works behind proxies and CDNs.
    """

    ip, is_routable = get_client_ip(request)
    if settings.DEBUG:
        print(f"Client IP: {ip}, Is routable: {is_routable}")  # Debug
    return ip if ip and is_routable else None

def get_city_by_ip(ip: str | None) -> str | None:
    """Return city name or None for invalid/unknown IP."""
    if not ip:
        return None
    try:
        geoip_instance = _geoip()
        result = geoip_instance.city(ip)
        if settings.DEBUG:
            print(f"Full GeoIP result: {result}")  # Debug - show full result
        city = result.get("city")
        if settings.DEBUG:
            print(f"GeoIP city lookup result: {city}")  # Debug
        return city
    except Exception as e:
        if settings.DEBUG:
            print(f"GeoIP error for IP {ip}: {e}")  # Debug - show IP
        return None

def index(request):
    """
    Return city name based on client IP.
    In DEBUG mode on localhost, use test IP for GeoIP lookup when real IP is not available.
    """
    ip = get_client_ip_address(request)
    if settings.DEBUG:
        print(f"Client IP address: {ip}")  # Debug

        # In local development, use test IP if real IP is not available
    if settings.DEBUG and not ip:
        test_ip = os.getenv('DEV_TEST_IP')
        if settings.DEBUG:
            print(f"DEBUG mode: using test IP {test_ip} for GeoIP lookup")  # Debug
        city = get_city_by_ip(test_ip)
        # If GeoIP doesn't return a city, use default fallback
        if not city:
            city = "Helsinki"
            if settings.DEBUG:
                print("DEBUG mode: GeoIP didn't return city, using fallback 'Helsinki'")
    else:
        city = get_city_by_ip(ip)
        # If no city found in production, use Helsinki fallback
        if not city:
            city = "Helsinki"
            if settings.DEBUG:
                print("No city found for IP, using fallback city: Helsinki")

    if settings.DEBUG:
        print(f"City determined from request: {city}")  # Debug
    return city
