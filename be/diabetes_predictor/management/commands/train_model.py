from django.core.management.base import BaseCommand
from ..ml_models.diabetes_model import train_model

class Command(BaseCommand):
    help = 'Train a new model using the latest data'

    def handle(self, *args, **options):
        result = train_model()
        
        if result['status'] == 'success':
            self.stdout.write(self.style.SUCCESS(f"Successfully trained new model:"))
            self.stdout.write(f"Version: {result['version']}")
            self.stdout.write(f"Train Accuracy: {result['train_accuracy']:.4f}")
            self.stdout.write(f"Test Accuracy: {result['test_accuracy']:.4f}")
            self.stdout.write(f"Model saved to: {result['model_path']}")
        else:
            self.stdout.write(self.style.ERROR(f"Error training model: {result['message']}"))
