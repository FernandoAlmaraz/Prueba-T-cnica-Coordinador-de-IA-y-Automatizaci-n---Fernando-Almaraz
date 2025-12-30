# OpenWeatherMap Service
import httpx
from typing import Optional
from app.config import get_settings
from app.models.schemas import WeatherResponse


class WeatherService:
    """Service for interacting with OpenWeatherMap API"""
    
    def __init__(self):
        self.settings = get_settings()
        self.base_url = self.settings.openweather_base_url
        self.api_key = self.settings.openweather_api_key
    
    async def get_weather(self, city: str, country_code: Optional[str] = None) -> WeatherResponse:
        """
        Get current weather for a city
        
        Args:
            city: City name
            country_code: Optional ISO 3166 country code
            
        Returns:
            WeatherResponse with current weather data
            
        Raises:
            httpx.HTTPStatusError: If the API request fails
        """
        # Build location query
        location = f"{city},{country_code}" if country_code else city
        
        # Make API request
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/weather",
                params={
                    "q": location,
                    "appid": self.api_key,
                    "units": "metric"  # Use Celsius
                }
            )
            response.raise_for_status()
            data = response.json()
        
        # Parse response into schema
        return WeatherResponse(
            city=data["name"],
            country=data["sys"]["country"],
            temperature=data["main"]["temp"],
            feels_like=data["main"]["feels_like"],
            description=data["weather"][0]["description"],
            humidity=data["main"]["humidity"],
            wind_speed=data["wind"]["speed"]
        )
