from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ============== REQUEST SCHEMAS ==============

class WeatherRequest(BaseModel):
    """Schema para solicitud de análisis de clima."""
    
    city: str = Field(..., min_length=1, max_length=100, examples=["La Paz"])
    country: Optional[str] = Field(None, min_length=2, max_length=2, examples=["BO"])
    
    class Config:
        json_schema_extra = {
            "example": {
                "city": "La Paz",
                "country": "BO"
            }
        }


# ============== RESPONSE SCHEMAS ==============

class Coordinates(BaseModel):
    """Coordenadas geográficas."""
    lat: float
    lon: float


class Location(BaseModel):
    """Información de ubicación."""
    city: str
    country: str
    coordinates: Coordinates


class WeatherData(BaseModel):
    """Datos del clima."""
    temperature: float = Field(..., description="Temperatura en Celsius")
    feels_like: float = Field(..., description="Sensación térmica en Celsius")
    temp_min: float = Field(..., description="Temperatura mínima")
    temp_max: float = Field(..., description="Temperatura máxima")
    humidity: int = Field(..., description="Humedad en porcentaje")
    pressure: int = Field(..., description="Presión atmosférica en hPa")
    description: str = Field(..., description="Descripción del clima")
    wind_speed: float = Field(..., description="Velocidad del viento en m/s")
    clouds: int = Field(..., description="Nubosidad en porcentaje")
    visibility: Optional[int] = Field(None, description="Visibilidad en metros")


class AIAnalysis(BaseModel):
    """Análisis generado por IA."""
    summary: str = Field(..., description="Resumen del clima")
    recommendations: List[str] = Field(..., description="Recomendaciones para el día")
    risk_level: str = Field(..., description="Nivel de riesgo: low, medium, high")
    risk_factors: List[str] = Field(default=[], description="Factores de riesgo identificados")


class Metadata(BaseModel):
    """Metadatos de la respuesta."""
    weather_fetch_ms: int = Field(..., description="Tiempo de consulta al API de clima")
    ai_analysis_ms: Optional[int] = Field(None, description="Tiempo de análisis de IA")
    total_ms: int = Field(..., description="Tiempo total de procesamiento")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class WeatherResponse(BaseModel):
    """Respuesta completa del análisis de clima."""
    
    location: Location
    weather: WeatherData
    ai_analysis: Optional[AIAnalysis] = None
    metadata: Metadata
    
    class Config:
        json_schema_extra = {
            "example": {
                "location": {
                    "city": "La Paz",
                    "country": "BO",
                    "coordinates": {"lat": -16.5, "lon": -68.15}
                },
                "weather": {
                    "temperature": 12.5,
                    "feels_like": 11.2,
                    "temp_min": 10.0,
                    "temp_max": 15.0,
                    "humidity": 35,
                    "pressure": 1013,
                    "description": "parcialmente nublado",
                    "wind_speed": 2.1,
                    "clouds": 40,
                    "visibility": 10000
                },
                "ai_analysis": {
                    "summary": "Clima fresco y agradable en La Paz con cielos parcialmente nublados.",
                    "recommendations": [
                        "Llevar una chaqueta ligera",
                        "Buen día para actividades al aire libre",
                        "Mantenerse hidratado por la altura"
                    ],
                    "risk_level": "low",
                    "risk_factors": []
                },
                "metadata": {
                    "weather_fetch_ms": 245,
                    "ai_analysis_ms": 1823,
                    "total_ms": 2068,
                    "timestamp": "2024-12-30T10:30:00Z"
                }
            }
        }


# ============== ERROR SCHEMAS ==============

class ErrorResponse(BaseModel):
    """Schema para respuestas de error."""
    
    error: str
    detail: str
    status_code: int