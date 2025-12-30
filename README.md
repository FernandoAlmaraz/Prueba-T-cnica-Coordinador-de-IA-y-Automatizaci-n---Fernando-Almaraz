# Ejercicio 1 - Microservicio Weather Analysis API

API REST construida con FastAPI que consulta datos del clima desde OpenWeatherMap y genera analisis inteligente utilizando Google Gemini.

## Tecnologias

- Python 3.12
- FastAPI
- Docker y Docker Compose
- OpenWeatherMap API
- Google Gemini AI

## Estructura del Proyecto
Creado con la estructura sugerida por FastAPI, Layered Architecture y Docker.
```
ejercicio-1-microservicio/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py
│   ├── routers/
│   │   ├── __init__.py
│   │   └── weather.py
│   └── services/
│       ├── __init__.py
│       ├── weather_service.py
│       └── ai_service.py
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Requisitos Previos

- Docker y Docker Compose instalados
- API Key de OpenWeatherMap (gratuita): https://openweathermap.org/api
- API Key de Google Gemini: https://aistudio.google.com/app/apikey

## Configuracion

1. Clonar el repositorio e ingresar al directorio del ejercicio:
```bash
cd ejercicio-1-microservicio
```

2. Crear el archivo de variables de entorno:
```bash
cp .env.example .env
```

3. Editar el archivo `.env` con tus API keys:
```
OPENWEATHER_API_KEY=tu_api_key_de_openweathermap
GEMINI_API_KEY=tu_api_key_de_gemini
```

## Ejecucion con Docker

### Construir y ejecutar
```bash
docker compose up --build
```

### Ejecutar en segundo plano
```bash
docker compose up -d --build
```

### Detener los contenedores
```bash
docker compose down
```

### Ver logs
```bash
docker compose logs -f
```

## Endpoints

La API expone los siguientes endpoints:

### Health Check

Verifica que el servicio este funcionando.
```
GET /api/v1/weather/health
```

Respuesta:
```json
{
    "status": "healthy",
    "service": "weather",
    "timestamp": "2024-12-30T10:30:00.000000"
}
```

### Obtener Clima Actual

Obtiene datos del clima sin analisis de IA.
```
POST /api/v1/weather/current
Content-Type: application/json
```

Request body:
```json
{
    "city": "La Paz",
    "country": "BO"
}
```

El campo `country` es opcional. Utiliza el codigo ISO de 2 letras del pais.

### Analizar Clima con IA

Obtiene datos del clima y genera analisis inteligente con Gemini.
```
POST /api/v1/weather/analyze
Content-Type: application/json
```

Request body:
```json
{
    "city": "La Paz",
    "country": "BO"
}
```

Respuesta:
```json
{
    "location": {
        "city": "La Paz",
        "country": "BO",
        "coordinates": {
            "lat": -16.5,
            "lon": -68.15
        }
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
            "Buen dia para actividades al aire libre",
            "Mantenerse hidratado por la altura"
        ],
        "risk_level": "low",
        "risk_factors": []
    },
    "metadata": {
        "weather_fetch_ms": 245,
        "ai_analysis_ms": 1823,
        "total_ms": 2068,
        "timestamp": "2024-12-30T10:30:00.000000"
    }
}
```

## Documentacion Interactiva

Una vez que la aplicacion este ejecutandose, puedes acceder a la documentacion interactiva:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Arquitectura

La aplicacion sigue una arquitectura modular:

- **config.py**: Configuracion centralizada usando pydantic-settings
- **models/**: Schemas de Pydantic para validacion de request y response
- **services/**: Logica de negocio separada en servicios independientes
  - `weather_service.py`: Integracion con OpenWeatherMap
  - `ai_service.py`: Integracion con Google Gemini
- **routers/**: Definicion de endpoints de la API

## Variables de Entorno

| Variable | Descripcion | Requerida |
|----------|-------------|-----------|
| OPENWEATHER_API_KEY | API key de OpenWeatherMap | Si |
| GEMINI_API_KEY | API key de Google Gemini | Si |
| APP_NAME | Nombre de la aplicacion | No |
| APP_VERSION | Version de la aplicacion | No |
| DEBUG | Modo debug | No |

## Manejo de Errores

La API retorna errores estructurados:

| Codigo | Descripcion |
|--------|-------------|
| 404 | Ciudad no encontrada |
| 401 | API key invalida |
| 503 | Error de conexion con servicios externos |
| 504 | Timeout en la consulta |

Ejemplo de respuesta de error:
```json
{
    "detail": "Ciudad no encontrada: InvalidCity"
}
```