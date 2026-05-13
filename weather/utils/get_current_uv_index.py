import requests

def get_current_uv_index(openweathermap_api_key: str, lat: float, lon: float):
    try:
        url = f'http://api.openweathermap.org/data/2.5/uvi?appid={openweathermap_api_key}&lat={lat}&lon={lon}'
        response = requests.get(url).json()
        return response['value']  # Returns the UV index value from the response
    except Exception as e:
        return "N/A"
