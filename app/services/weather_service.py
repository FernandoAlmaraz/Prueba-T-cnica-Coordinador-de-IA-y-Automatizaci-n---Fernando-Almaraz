import httpx
from typing import Optional
import time

from app.config import get_settings
from app.models import WeatherData, Location, Coordinates


class WeatherServiceError(Exception):
    """Excepción personalizada para errores del servicio de clima."""
    
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class WeatherService:
    """Servicio para obtener datos del clima desde OpenWeatherMap."""
    
    def __init__(self):
        self.settings = get_settings()
        self.base_url = self.settings.openweather_base_url
        self.api_key = self.settings.openweather_api_key
        self.timeout = self.settings.openweather_timeout
    
    async def get_weather(
        self, 
        city: str, 
        country: Optional[str] = None
    ) -> tuple[Location, WeatherData, int]:
        """
        Obtiene datos del clima para una ciudad.
        
        Args:
            city: Nombre de la ciudad
            country: Código ISO del país (opcional, ej: "BO")
            
        Returns:
            Tupla con (Location, WeatherData, tiempo_ms)
            
        Raises:
            WeatherServiceError: Si hay error en la consulta
        """
        # Construir query de ubicación
        location_query = f"{city},{country}" if country else city
        
        # Parámetros de la API
        params = {
            "q": location_query,
            "appid": self.api_key,
            "units": "metric",  # Celsius
            "lang": "es"        # Respuestas en español
        }
        
        start_time = time.perf_counter()
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(
                    f"{self.base_url}/weather",
                    params=params
                )
                
                elapsed_ms = int((time.perf_counter() - start_time) * 1000)
                
                # Manejar errores de la API
                if response.status_code == 404:
                    raise WeatherServiceError(
                        f"Ciudad no encontrada: {city}",
                        status_code=404
                    )
                elif response.status_code == 401:
                    raise WeatherServiceError(
                        "API key inválida o no autorizada",
                        status_code=401
                    )
                elif response.status_code != 200:
                    raise WeatherServiceError(
                        f"Error en API de clima: {response.status_code}",
                        status_code=response.status_code
                    )
                
                data = response.json()
                
                # Parsear respuesta
                location = Location(
                    city=data["name"],
                    country=data["sys"]["country"],
                    coordinates=Coordinates(
                        lat=data["coord"]["lat"],
                        lon=data["coord"]["lon"]
                    )
                )
                
                weather = WeatherData(
                    temperature=data["main"]["temp"],
                    feels_like=data["main"]["feels_like"],
                    temp_min=data["main"]["temp_min"],
                    temp_max=data["main"]["temp_max"],
                    humidity=data["main"]["humidity"],
                    pressure=data["main"]["pressure"],
                    description=data["weather"][0]["description"],
                    wind_speed=data["wind"]["speed"],
                    clouds=data["clouds"]["all"],
                    visibility=data.get("visibility")
                )
                
                return location, weather, elapsed_ms
                
            except httpx.TimeoutException:
                raise WeatherServiceError(
                    "Timeout al consultar API de clima",
                    status_code=504
                )
            except httpx.RequestError as e:
                raise WeatherServiceError(
                    f"Error de conexión: {str(e)}",
                    status_code=503
                )


# Singleton del servicio
_weather_service: Optional[WeatherService] = None


def get_weather_service() -> WeatherService:
    """Obtiene instancia singleton del servicio de clima."""
    global _weather_service
    if _weather_service is None:
        _weather_service = WeatherService()
    return _weather_service