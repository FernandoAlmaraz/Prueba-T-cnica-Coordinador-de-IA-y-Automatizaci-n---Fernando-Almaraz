import google.generativeai as genai
from typing import Optional
import time
import json

from app.config import get_settings
from app.models import WeatherData, Location


class AIServiceError(Exception):
    """Excepción personalizada para errores del servicio de IA."""
    
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class AIService:
    """Servicio para análisis de clima con Google Gemini."""
    
    def __init__(self):
        self.settings = get_settings()
        genai.configure(api_key=self.settings.gemini_api_key)
        self.model = genai.GenerativeModel(self.settings.gemini_model)
    
    async def analyze_weather(
        self,
        location: Location,
        weather: WeatherData
    ) -> tuple[dict, int]:
        """
        Analiza los datos del clima usando Gemini.
        
        Args:
            location: Datos de ubicación
            weather: Datos del clima
            
        Returns:
            Tupla con (análisis, tiempo_ms)
            
        Raises:
            AIServiceError: Si hay error en el análisis
        """
        prompt = self._build_prompt(location, weather)
        
        start_time = time.perf_counter()
        
        try:
            response = self.model.generate_content(prompt)
            elapsed_ms = int((time.perf_counter() - start_time) * 1000)
            
            # Parsear respuesta JSON
            analysis = self._parse_response(response.text)
            
            return analysis, elapsed_ms
            
        except json.JSONDecodeError as e:
            raise AIServiceError(
                f"Error parseando respuesta de IA: {str(e)}",
                status_code=500
            )
        except Exception as e:
            raise AIServiceError(
                f"Error en análisis de IA: {str(e)}",
                status_code=503
            )
    
    def _build_prompt(self, location: Location, weather: WeatherData) -> str:
        """Construye el prompt para Gemini."""
        return f"""Analiza los siguientes datos del clima y responde ÚNICAMENTE con un JSON válido, sin markdown ni texto adicional.

DATOS DEL CLIMA:
- Ciudad: {location.city}, {location.country}
- Temperatura: {weather.temperature}°C
- Sensación térmica: {weather.feels_like}°C
- Humedad: {weather.humidity}%
- Presión: {weather.pressure} hPa
- Descripción: {weather.description}
- Viento: {weather.wind_speed} m/s
- Nubosidad: {weather.clouds}%
- Visibilidad: {weather.visibility} metros

Responde con este formato JSON exacto:
{{
    "summary": "Resumen breve del clima actual en 1-2 oraciones",
    "recommendations": ["recomendación 1", "recomendación 2", "recomendación 3"],
    "risk_level": "low|medium|high",
    "risk_factors": ["factor 1 si aplica"]
}}

REGLAS:
- summary: Describe el clima de forma natural y útil
- recommendations: 3 recomendaciones prácticas para el día
- risk_level: "low" para clima agradable, "medium" para precaución, "high" para condiciones extremas
- risk_factors: Lista vacía si risk_level es "low", factores de riesgo si es medium/high

JSON:"""

    def _parse_response(self, response_text: str) -> dict:
        """Parsea la respuesta de Gemini a un diccionario."""
        # Limpiar posibles caracteres extra
        cleaned = response_text.strip()
        
        # Remover backticks de markdown si existen
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        
        cleaned = cleaned.strip()
        
        return json.loads(cleaned)


# Singleton del servicio
_ai_service: Optional[AIService] = None


def get_ai_service() -> AIService:
    """Obtiene instancia singleton del servicio de IA."""
    global _ai_service
    if _ai_service is None:
        _ai_service = AIService()
    return _ai_service