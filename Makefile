.PHONY: clean-db init-db compose-up import-data fresh-start

# Clean the source database
clean-db:
	docker exec -i source_db psql -U postgres -c "DROP DATABASE IF EXISTS source_db;"
	docker exec -i source_db psql -U postgres -c "CREATE DATABASE source_db;"

# Initialize the source database
init-db:
	docker-compose run --rm backend python manage.py init_source_db

# Start all services
compose-up:
	docker-compose up -d

# Import data from source to web database
import-data:
	docker-compose run --rm backend python manage.py import_data

# Fresh start: clean, init, start and import
fresh-start: clean-db init-db compose-up import-data
	@echo "Fresh start completed!"

# Stop all services
stop:
	docker-compose down

# Remove all containers and volumes
reset:
	docker-compose down -v

# Build frontend
build-frontend:
	docker-compose build frontend

# Start backend in development mode
start-backend:
	docker-compose run --rm backend python manage.py runserver 0.0.0.0:8000

# Start frontend in development mode
start-frontend:
	docker-compose run --rm frontend npm start
