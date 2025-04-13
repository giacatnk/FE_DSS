from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, AlertViewSet, ModelViewSet

router = DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'alerts', AlertViewSet)
router.register(r'models', ModelViewSet, basename='model')

urlpatterns = [
    path('', include(router.urls)),
]