from fastapi import APIRouter, HTTPException
from datetime import datetime
import time

from app.models import WeatherRequest, WeatherResponse, Metadata, ErrorResponse
from app.services import get_weather_service, WeatherServiceError


router = APIRouter(prefix="/api/v1/weather", tags=["Weather"])


@router.post(
    "/analyze",
    response_model=WeatherResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Ciudad no encontrada"},
        503: {"model": ErrorResponse, "description": "Error de conexión"},
        504: {"model": ErrorResponse, "description": "Timeout"}
    },
    summary="Analizar clima de una ciudad",
    description="Obtiene datos del clima para una ciudad específica usando OpenWeatherMap."
)
async def analyze_weather(request: WeatherRequest) -> WeatherResponse:
    """
    Endpoint para obtener y analizar el clima de una ciudad.
    
    - **city**: Nombre de la ciudad (requerido)
    - **country**: Código ISO de 2 letras del país (opcional, ej: BO, US, ES)
    """
    start_time = time.perf_counter()
    
    weather_service = get_weather_service()
    
    try:
        location, weather, weather_fetch_ms = await weather_service.get_weather(
            city=request.city,
            country=request.country
        )
        
        total_ms = int((time.perf_counter() - start_time) * 1000)
        
        return WeatherResponse(
            location=location,
            weather=weather,
            metadata=Metadata(
                weather_fetch_ms=weather_fetch_ms,
                total_ms=total_ms,
                timestamp=datetime.utcnow()
            )
        )
        
    except WeatherServiceError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )


@router.get(
    "/health",
    summary="Health check",
    description="Verifica que el servicio de clima esté funcionando."
)
async def health_check():
    """Health check del servicio."""
    return {
        "status": "healthy",
        "service": "weather",
        "timestamp": datetime.utcnow().isoformat()
    }