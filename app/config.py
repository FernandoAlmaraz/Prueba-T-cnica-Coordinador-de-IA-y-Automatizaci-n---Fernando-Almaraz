from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Configuración de la aplicación usando variables de entorno."""
    
    # API Keys
    openweather_api_key: str
    
    # OpenWeatherMap Config
    openweather_base_url: str = "https://api.openweathermap.org/data/2.5"
    openweather_timeout: float = 10.0
    
    # App Config
    app_name: str = "Weather Analysis API"
    app_version: str = "1.0.0"
    debug: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Retorna configuración cacheada (singleton)."""
    return Settings()