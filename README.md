# Data Ingestion Service - Microservices Architecture

Este proyecto implementa un servicio de ingesta de datos utilizando una arquitectura de microservicios que se comunican a través de Apache Pulsar, siguiendo los principios de la arquitectura hexagonal (puertos y adaptadores).

## Arquitectura

El sistema está compuesto por los siguientes microservicios:

1. **Servicio de Ingesta (Ingestion Service)**: Recibe datos de socios externos y los almacena en la base de datos.
2. **Servicio de Consulta (Query Service)**: Proporciona endpoints para consultar los datos almacenados.
3. **Servicio de Procesamiento (Processing Service)**: Procesa los datos ingresados y genera resultados.
4. **Servicio de Validación (Validation Service)**: Valida los datos ingresados según reglas de negocio.

Los microservicios se comunican entre sí mediante eventos publicados en Apache Pulsar, lo que permite un acoplamiento débil y una alta escalabilidad.

## Topología de Administración de Datos

### Topología Descentralizada

Este proyecto implementa una **topología descentralizada** para la administración de datos, donde cada microservicio gestiona su propio almacenamiento de datos. Esta decisión se justifica por las siguientes razones:

1. **Alta autonomía**: Cada servicio puede evolucionar independientemente sin afectar a otros.
2. **Escalabilidad independiente**: Los servicios pueden escalar según sus propias necesidades.
3. **Aislamiento de fallos**: Los problemas en un servicio no afectan directamente a otros.
4. **Especialización de almacenamiento**: Cada servicio puede utilizar el tipo de base de datos más adecuado para sus necesidades específicas.

Aunque esta topología introduce desafíos como la consistencia eventual y la complejidad en consultas que cruzan servicios, estos se mitigan mediante el uso de eventos de dominio que mantienen la coherencia entre servicios.

## Modelo de Persistencia de Datos

### Event Sourcing

Hemos implementado el modelo de **Event Sourcing** en nuestros microservicios, lo que significa que:

1. Todos los cambios en el estado de la aplicación se capturan como una secuencia de eventos.
2. Estos eventos se almacenan en un registro inmutable (event store).
3. El estado actual se puede reconstruir reproduciendo los eventos.

Esta elección proporciona:

- **Trazabilidad completa**: Historial completo de todas las operaciones y cambios.
- **Capacidad de auditoría**: Facilita cumplir con requisitos regulatorios.
- **Reconstrucción de estados pasados**: Posibilidad de "viajar en el tiempo" para análisis o depuración.
- **Desacoplamiento**: Separación clara entre la captura de eventos y su procesamiento.

### Implementación en los Servicios

#### 1. Servicio de Ingesta

- Captura eventos `DataReceived` cuando se reciben datos de socios.
- Almacena estos eventos en un event store antes de cualquier procesamiento.
- Publica eventos `DataIngested` para notificar a otros servicios.

#### 2. Servicio de Consulta

- Mantiene una vista materializada optimizada para consultas.
- Se suscribe a eventos `DataIngested`, `DataProcessed` y `DataValidated` para actualizar sus vistas.
- Proporciona APIs para consultar datos sin acceder directamente a los event stores de otros servicios.

#### 3. Servicio de Procesamiento

- Consume eventos `DataIngested` para iniciar el procesamiento.
- Registra cada paso del procesamiento como eventos.
- Publica eventos `DataProcessed` con los resultados.

#### 4. Servicio de Validación

- Consume eventos `DataIngested` para validar los datos.
- Registra los resultados de validación como eventos.
- Publica eventos `DataValidated` con el estado de validación.

## Eventos del Dominio

- **DataIngested**: Se publica cuando se ingresan nuevos datos.
- **DataProcessed**: Se publica cuando los datos han sido procesados.
- **DataValidated**: Se publica cuando los datos han sido validados.

## Tecnologías Utilizadas

- **Python**: Lenguaje de programación principal.
- **Flask**: Framework web para los endpoints HTTP.
- **SQLAlchemy**: ORM para la persistencia de datos.
- **Apache Pulsar**: Sistema de mensajería para la comunicación entre microservicios.
- **Docker**: Contenedorización de los microservicios.
- **PostgreSQL**: Base de datos relacional.

## Estructura del Proyecto

ingestion_service/
├── domain/ # Capa de dominio (entidades, eventos, etc.)
├── application/ # Capa de aplicación (servicios, comandos, consultas)
├── infrastructure/ # Capa de infraestructura (implementaciones concretas)
├── microservices/ # Implementaciones de microservicios
│ ├── ingestion_service/ # Servicio de ingesta
│ ├── query_service/ # Servicio de consulta
│ ├── processing_service/ # Servicio de procesamiento
│ └── validation_service/ # Servicio de validación
├── docker-compose.yml # Configuración de Docker Compose
└── requirements.txt # Dependencias del proyecto

## Instalación y Ejecución

### Requisitos Previos

- Docker y Docker Compose
- Python 3.9 o superior (para desarrollo local)

### Ejecución con Docker Compose

1. Clonar el repositorio:

   ```bash
   git clone <url-del-repositorio>
   cd ingestion_service
   ```

2. Iniciar los servicios con Docker Compose:

   ```bash
   docker-compose up -d
   ```

3. Verificar que los servicios estén funcionando:
   ```bash
   docker-compose ps
   ```

### Desarrollo Local

1. Crear un entorno virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

2. Instalar dependencias:

   ```bash
   pip install -r requirements.txt
   ```

3. Iniciar Apache Pulsar localmente:

   ```bash
   docker-compose up -d pulsar postgres
   ```

4. Ejecutar los microservicios individualmente:
   ```bash
   python microservices/ingestion_service/main.py
   python microservices/query_service/main.py
   python microservices/processing_service/main.py
   python microservices/validation_service/main.py
   ```

## API Endpoints

### Servicio de Ingesta (puerto 5001)

- `POST /ingest`: Ingesta nuevos datos
  ```json
  {
    "partner_id": "partner123",
    "payload": {
      "name": "Example Data",
      "age": 30,
      "attributes": {
        "key1": "value1",
        "key2": "value2"
      }
    }
  }
  ```

### Servicio de Consulta (puerto 5002)

- `GET /query/{data_id}`: Obtiene datos por ID
- `GET /query/partner/{partner_id}`: Obtiene todos los datos de un socio específico
- `GET /query/all`: Obtiene todos los datos ingresados

## Configuración

La configuración se realiza principalmente a través de variables de entorno:

- `PULSAR_SERVICE_URL`: URL del servicio de Apache Pulsar (por defecto: `pulsar://localhost:6650`)
- `DATABASE_URL`: URL de conexión a la base de datos PostgreSQL
- `PORT`: Puerto para los servicios web (por defecto: 5001 para ingesta, 5002 para consulta)

## Arquitectura Hexagonal

Este proyecto sigue los principios de la arquitectura hexagonal:

- **Capa de Dominio**: Contiene las entidades, eventos y reglas de negocio.
- **Capa de Aplicación**: Implementa los casos de uso mediante servicios, comandos y consultas.
- **Capa de Infraestructura**: Proporciona implementaciones concretas para los puertos definidos en el dominio.
