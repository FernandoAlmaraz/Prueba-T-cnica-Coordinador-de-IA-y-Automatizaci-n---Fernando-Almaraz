# Ejercicio 3 - Diseño de Asistente basado en RAG

Propuesta de arquitectura para un asistente interno de IA que responde consultas sobre documentación técnica de la empresa, aplicando el patrón Retrieval-Augmented Generation (RAG).

## Contenido del Entregable

```
Ejercicio 3/
├── Propuesta-Arquitectura-RAG.pdf    # Documento principal
├── README.md                           # Este archivo
└── diagramas/
    ├── arquitectura-onpremise.drawio   # Diagrama editable On-Premise
    ├── arquitectura-cloud-gcp.drawio   # Diagrama editable Cloud

└── screenshots/
    ├── arquitectura-onpremise.png      # Diagrama exportado
    └── arquitectura-cloud-gcp.png      # Diagrama exportado
```

## Resumen de la Propuesta

### Problema a Resolver

Las empresas tienen documentación dispersa en múltiples plataformas (Confluence, Google Drive, repositorios Git, CRMs, hojas de cálculo). Los empleados pierden tiempo buscando información y haciendo preguntas repetitivas.

### Solución

Un asistente de IA basado en RAG que:

- Centraliza la búsqueda de documentación
- Responde preguntas en lenguaje natural
- Cita las fuentes de información
- Respeta permisos de acceso por rol
- Se integra con sistemas en tiempo real (Jira, GitLab)

## Arquitecturas Propuestas

### Opción 1: On-Premise (Self-hosted)

| Componente | Tecnología |
|------------|------------|
| Extracción de texto | Unstructured |
| Orquestación | LangChain |
| Embeddings | Sentence Transformers |
| Vector Store | Qdrant (Docker) |
| LLM | Ollama + Llama 3 |
| Backend | FastAPI |
| Autenticación | JWT / Keycloak |

**Ventajas**: Privacidad total, sin costos recurrentes, control completo

**Ideal para**: Empresas con datos sensibles, equipos técnicos fuertes

### Opción 2: Cloud (Google Cloud Platform)

| Componente | Servicio GCP |
|------------|--------------|
| Extracción de texto | Document AI |
| Orquestación | Vertex AI Pipelines |
| Embeddings | Vertex AI Embeddings |
| Vector Store | Vertex AI Vector Search |
| LLM | Gemini Pro |
| Backend | Cloud Run |
| Autenticación | Identity-Aware Proxy |

**Ventajas**: Sin mantenimiento, escalabilidad automática, setup rápido

**Ideal para**: Startups, empresas sin equipo DevOps, usuarios de Google Workspace

## Fuentes de Datos Soportadas

| Área | Contenido | Formato/Origen |
|------|-----------|----------------|
| Desarrollo | Estándares, guías, APIs | Markdown, Confluence, Swagger |
| Ventas | Procesos, comisiones | Excel, CRM, Google Sheets |
| Productos | Catálogos, precios | PDF, Excel |
| RRHH | Políticas, beneficios | Excel, PDF |
| Legal | Contratos, términos | PDF, Word |

## Seguridad

- **Middleware de validación**: Rechaza solicitudes no autorizadas antes de procesar
- **Autenticación**: JWT/Keycloak (On-Premise) o IAP (Cloud)
- **Autorización por roles**: Filtrado de documentos según permisos
- **Auditoría**: Registro de todas las consultas

## Diagramas

Los diagramas están en formato `.drawio` y pueden editarse en:

- Web: https://app.diagrams.net
- Desktop: Aplicación draw.io

Para exportar a PNG: File → Export as → PNG

## Estructura del Documento Principal

1. Introducción (Qué es RAG - Analogía de la Biblioteca)
2. Fuentes de Datos
3. Pipeline de Ingesta
4. Arquitectura On-Premise
5. Arquitectura Cloud (GCP)
6. Flujo de Consulta
7. Seguridad y Control de Acceso
8. Control de Relevancia
9. Ventajas y Limitaciones
10. Comparativa de Arquitecturas
11. Recomendación Final

## Autor

Ing. Fernando Gabriel Almaraz De La Quintana

Diciembre 2025