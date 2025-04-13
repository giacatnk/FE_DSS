diabetes_api/
├── config/                  # Django project settings
│   ├── __init__.py
│   ├── settings.py          # Project settings
│   ├── urls.py              # Main URL routing
│   ├── asgi.py
│   └── wsgi.py
├── diabetes_predictor/      # Main app
│   ├── __init__.py
│   ├── admin.py             # Admin interface config
│   ├── apps.py
│   ├── models.py            # Database models
│   ├── serializers.py       # DRF serializers
│   ├── views.py             # API views
│   ├── urls.py              # App URL routing
│   ├── ml_models/           # ML model storage
│   │   ├── __init__.py
│   │   ├── diabetes_model.py  # Model implementation
│   │   └── model.pkl         # Trained model file
│   └── tests.py             # Tests
├── manage.py                # Django management script
├── requirements.txt         # Dependencies
└── README.md                # Project documentation