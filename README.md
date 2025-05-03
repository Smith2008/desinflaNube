# Simetrik Cost Optimization

Este proyecto contiene:

- **frontend/**: Aplicación ReactJS para visualizar costos.
- **backend/**: API en Django + DRF que expone datos de costos.
- **billing-api/**: Servicio en Go que extrae billing de AWS y alimenta la base de datos PostgreSQL.

## Cómo ejecutar

1. Clonar el repositorio.
2. Configurar variables de entorno y credenciales AWS.
3. Levantar PostgreSQL y aplicar migraciones:

   ```bash
   cd backend
   pip install -r requirements.txt
   python manage.py migrate
   ```

4. Ejecutar el extractor Go:

   ```bash
   cd billing-api
   go run main.go
   ```

5. Iniciar Django y React:

   ```bash
   # En backend
   python manage.py runserver

   # En frontend
   cd ../frontend
   npm install
   npm start
   ```
