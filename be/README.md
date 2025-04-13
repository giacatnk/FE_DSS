# Diabetes Prediction API

## Overview
This project provides a Django-based API for diabetes prediction, integrated with an external ML service for predictions and model training.

## Requirements

### Local Development
1. Python 3.9+
2. Docker and Docker Compose (optional)

### Python Dependencies
- Django >= 4.2.10
- requests >= 2.32.3
- pandas >= 2.1.0
- scikit-learn >= 1.3.0
- numpy >= 1.24.3

## Setup Instructions

### Using Docker (Recommended)
1. Install Docker and Docker Compose
2. Clone the repository
3. Build and start the container:
   ```bash
   docker-compose up --build
   ```
4. Create and apply migrations:
   ```bash
   docker-compose exec web python manage.py migrate
   ```
5. Create a superuser (optional):
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

### Local Development
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the database:
   ```bash
   python manage.py migrate
   ```
4. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```
5. Run the development server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Patients
- `GET /api/patients/` - List all patients
- `POST /api/patients/` - Create a new patient
- `GET /api/patients/{id}/` - Retrieve a specific patient
- `PUT /api/patients/{id}/` - Update a patient
- `DELETE /api/patients/{id}/` - Delete a patient

### Alerts
- `GET /api/alerts/` - List all alerts
- `GET /api/alerts/{id}/` - Retrieve a specific alert
- `PUT /api/alerts/{id}/` - Update alert details (including is_correct)

### Models
- `POST /api/models/retrain/` - Retrain the model
- `GET /api/models/status/` - Get current model status
- `POST /api/models/predict/` - Make predictions for multiple patients

## Environment Variables

Create a `.env` file in the project root with the following variables:

```
DEBUG=1
SECRET_KEY=your-secret-key-here
```

## Running Tests

```bash
python manage.py test
```

## Project Structure

```
.
├── diabetes_predictor/          # Django app
│   ├── models.py              # Database models
│   ├── views.py               # API views
│   ├── serializers.py         # API serializers
│   └── ml_models/             # ML service integration
├── config/                    # Django project settings
│   ├── settings.py           # Django settings
│   └── urls.py              # URL configuration
├── requirements.txt           # Python dependencies
├── Dockerfile                # Docker configuration
└── docker-compose.yml        # Docker Compose configuration
```

## ML Service Requirements

The ML service is expected to be running externally on port 8080 with the following endpoints:

- `POST /predict` - Make predictions
- `POST /retrain` - Retrain the model
- `GET /status` - Get model status

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details