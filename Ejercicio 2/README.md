# Ejercicio 2 - Flujo de Automatizacion con n8n

Flujo de automatizacion low-code que consume el microservicio del Ejercicio 1, guarda los datos en Google Sheets y envia notificaciones por email.

## Tecnologias

- n8n (self-hosted con Docker)
- Google Sheets API
- Gmail SMTP

## Arquitectura del Flujo
```
[Trigger Diario 7AM] -> [Lista Ciudades Bolivia] -> [Consultar API Clima] -> [Guardar en Google Sheets] -> [Agrupar Resultados] -> [Notificar por Email]
```

## Descripcion de Nodos

### 1. Trigger Diario 7AM (Schedule Trigger)

- **Tipo**: Schedule Trigger
- **Configuracion**: Ejecucion diaria a las 7:00 AM
- **Zona horaria**: America/La_Paz

### 2. Lista Ciudades Bolivia (Code)

- **Tipo**: Code (JavaScript)
- **Funcion**: Genera una lista con las 9 capitales de departamento de Bolivia
- **Ciudades**:
  - La Paz
  - Cochabamba
  - Santa Cruz de la Sierra
  - Oruro
  - Potosi
  - Tarija
  - Sucre
  - Trinidad
  - Cobija

### 3. Consultar API Clima (HTTP Request)

- **Tipo**: HTTP Request
- **Metodo**: POST
- **URL**: http://weather-api:8000/api/v1/weather/analyze
- **Body**: JSON con ciudad y pais
- **Control de errores**:
  - Retry On Fail: Activado
  - Max Tries: 3
  - Wait Between Tries: 5000ms
  - On Error: Continue

### 4. Guardar en Google Sheets (Google Sheets)

- **Tipo**: Google Sheets
- **Operacion**: Append Row
- **Autenticacion**: Service Account
- **Documento**: Weather Data Bolivia
- **Columnas mapeadas**:
  - timestamp
  - city
  - country
  - temperature
  - humidity
  - description
  - wind_speed
  - ai_summary

### 5. Agrupar Resultados (Aggregate)

- **Tipo**: Aggregate
- **Funcion**: Agrupa los 9 resultados en un solo item para enviar un unico email

### 6. Notificar por Email (Send Email)

- **Tipo**: Email Send (SMTP)
- **Servidor**: smtp.gmail.com
- **Puerto**: 587
- **Contenido**: Notificacion con enlace al Google Sheet

## Requisitos Previos

### Google Cloud

1. Crear proyecto en Google Cloud Console
2. Habilitar Google Sheets API
3. Habilitar Google Drive API
4. Crear Service Account y descargar JSON de credenciales

### Google Sheets

1. Crear hoja "Weather Data Bolivia"
2. Agregar headers: timestamp, city, country, temperature, humidity, description, wind_speed, ai_summary
3. Compartir la hoja con el email del Service Account (permisos de Editor)

### Gmail

1. Activar verificacion en 2 pasos en la cuenta de Gmail
2. Generar contrasena de aplicacion en https://myaccount.google.com/apppasswords

## Configuracion en n8n

### Credenciales Google Sheets

1. Ir a Credentials -> Add Credential -> Google Sheets API
2. Seleccionar Service Account
3. Ingresar email del Service Account
4. Pegar Private Key del archivo JSON

### Credenciales SMTP

1. Ir a Credentials -> Add Credential -> SMTP
2. Configurar:
   - Host: smtp.gmail.com
   - Port: 587
   - SSL/TLS: STARTTLS
   - User: tu email de Gmail
   - Password: contrasena de aplicacion (16 caracteres)

## Ejecucion

### Importar el flujo

1. En n8n, ir a Workflows -> Import from File
2. Seleccionar el archivo `workflow.json`
3. Configurar las credenciales de Google Sheets y SMTP

### Ejecucion manual

1. Abrir el workflow
2. Click en "Test Workflow"

### Ejecucion automatica

1. Activar el workflow con el toggle en la esquina superior derecha
2. El flujo se ejecutara automaticamente cada dia a las 7:00 AM

## Control de Errores

El nodo HTTP Request tiene configurado:

- **Retry On Fail**: Si la API falla, reintenta hasta 3 veces
- **Wait Between Tries**: Espera 5 segundos entre cada intento
- **On Error Continue**: Si falla despues de 3 intentos, continua con la siguiente ciudad

Esto garantiza que:
- Errores temporales de red se recuperan automaticamente
- Una ciudad con error no bloquea el procesamiento de las demas

## Limitaciones

- El analisis de IA depende de la cuota disponible de Google Gemini (20 requests/dia en tier gratuito)
- Si se excede la cuota, el flujo continua guardando los datos del clima sin el analisis de IA

## Estructura de Archivos
```
ejercicio-2-n8n/
├── workflow.json          # Export del flujo de n8n
├── screenshots/
│   ├── 01-flujo-completo.png
│   ├── 02-google-sheets.png
│   └── 03-email-notificacion.png
└── README.md
```