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

## Cómo usar (Demo)

1. **Login**
   - Accede a la aplicación frontend en `http://localhost:3000`.
   - Introduce tus credenciales de usuario (se mostrará sesión iniciada correctamente).
2. **Ver Recomendaciones**
   - En el menú principal selecciona "Recomendaciones FinOps".
   - La lista mostrará sugerencias generadas por el bot (downsizing, Spot, storage, shutdown).
3. **Aplicar Ahorros**
   - Para cada recomendación verás un botón **"Aplicar"**.
   - Al hacer clic se invocará el playbook de Terraform/Harness vía Lambda.
   - Confirma la acción en el modal emergente.
4. **Validar Resultados**
   - Navega a "Historial de Ahorros" para ver las optimizaciones aplicadas.
   - Verifica en AWS Console o en el dashboard Datadog los cambios de instancia y costes.
