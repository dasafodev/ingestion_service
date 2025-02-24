# Servicio de Ingesta de Datos

Un servicio para ingerir y gestionar datos de varios socios, construido utilizando principios de Diseño Orientado a Dominio (DDD) y Arquitectura Hexagonal.

## Arquitectura

Este proyecto sigue una Arquitectura Hexagonal (Puertos y Adaptadores) con las siguientes capas:

- **Capa de Dominio**: Contiene la lógica empresarial central, entidades, objetos de valor y eventos de dominio.
- **Capa de Aplicación**: Contiene servicios de aplicación, comandos y consultas (patrón CQS).
- **Capa de Infraestructura**: Contiene implementaciones de repositorios, bus de eventos y puntos finales de API.

## Elementos de Diseño Orientado a Dominio

El servicio implementa los siguientes conceptos de DDD:

- **Entidades**: Objetos de dominio con identidad (por ejemplo, `IngestedData`)
- **Objetos de Valor**: Objetos inmutables sin identidad (por ejemplo, `PartnerId`, `Payload`, `Timestamp`)
- **Agregados**: Conjunto de objetos de dominio tratados como una unidad (por ejemplo, `IngestedData` como raíz de agregado)
- **Repositorios**: Abstracciones de persistencia (por ejemplo, `DataRepository`)
- **Eventos de Dominio**: Eventos que representan algo que sucedió en el dominio (por ejemplo, `DataIngested`)
- **Fábricas**: Objetos que crean objetos de dominio complejos (por ejemplo, `IngestedDataFactory`)

## Separación de Comandos y Consultas (CQS)

El servicio utiliza el patrón CQS para separar las operaciones que modifican el estado (comandos) de las operaciones que leen el estado (consultas):

- **Comandos**: `IngestDataCommand`
- **Consultas**: `GetDataByIdQuery`, `GetAllDataQuery`, `GetDataByPartnerIdQuery`

## Comunicación Basada en Eventos

La comunicación entre diferentes módulos se realiza a través de eventos de dominio:

1. Cuando se ingesta datos, se publica un evento `DataIngested`
2. Los suscriptores pueden reaccionar a estos eventos (por ejemplo, registro, procesamiento adicional)

## Base de Datos

El servicio utiliza SQLAlchemy para operaciones de base de datos, con soporte para:

- SQLite (predeterminado para desarrollo)

## Comenzando

### Requisitos Previos

- Python 3.9+
- PostgreSQL (opcional, SQLite se utiliza por defecto)

### Instalación

1. Clona el repositorio
2. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```
3. Configura la base de datos en el archivo `.env` (opcional)
4. Ejecuta la aplicación:
   ```
   python main.py
   ```

### Docker

Para ejecutar el servicio utilizando Docker:

```
docker build -t ingestion-service .
docker run -p 5001:5001 ingestion-service
```

## Puntos Finales de la API

- `POST /ingest`: Ingestar nuevos datos
- `GET /ingest/<data_id>`: Obtener datos por ID
- `GET /ingest/partner/<partner_id>`: Obtener todos los datos para un socio específico
- `GET /ingest/all`: Obtener todos los datos ingeridos
