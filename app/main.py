from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import get_settings
from app.routers import weather_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manejo del ciclo de vida de la aplicación."""
    # Startup
    settings = get_settings()
    print(f"🚀 Iniciando {settings.app_name} v{settings.app_version}")
    print(f"📍 OpenWeatherMap configurado")
    yield
    # Shutdown
    print("👋 Apagando aplicación...")


def create_app() -> FastAPI:
    """Factory para crear la aplicación FastAPI."""
    
    settings = get_settings()
    
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="""
## Weather Analysis API

API para obtener y analizar datos del clima usando OpenWeatherMap y análisis de IA.

### Funcionalidades:
- 🌤️ Consulta de clima por ciudad
- 🤖 Análisis inteligente con IA (próximamente)
- 📊 Métricas de rendimiento

### Uso:
Envía un POST a `/api/v1/weather/analyze` con el nombre de la ciudad.
        """,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # CORS - permitir todas las origenes para desarrollo
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Registrar routers
    app.include_router(weather_router)
    
    # Root endpoint
    @app.get("/", tags=["Root"])
    async def root():
        return {
            "name": settings.app_name,
            "version": settings.app_version,
            "docs": "/docs",
            "health": "/api/v1/weather/health"
        }
    
    return app


# Crear instancia de la app
app = create_app()