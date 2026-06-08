# proyecto_centro_salud

Proyecto con varios servicios Docker para gestión de centro de salud.

Estructura:
- app_agenda/
- app_frontend/
- app_laboratorio/
- app_tickets/
- db_init/
- nginx/

Cómo probar (local):

1. Construir y levantar con Docker Compose:

```bash
docker-compose up --build
```

2. Abrir `index.html` o acceder a los servicios según configuración de `nginx`.
