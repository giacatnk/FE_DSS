import logging
import schedule
import time
import threading
from src.trainer import ModelTrainer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TrainingScheduler:
    def __init__(self, trainer: ModelTrainer):
        self.trainer = trainer
        self.scheduler_thread = None

    def train_job(self):
        """Scheduled job to train the model."""
        logger.info("Starting scheduled model training")
        self.trainer.train_model()
        logger.info("Scheduled model training completed")

    def run_scheduler(self):
        """Run the training scheduler."""
        # Train immediately on startup
        self.train_job()
        
        # Schedule training every hour
        schedule.every(1).hours.do(self.train_job)
        
        logger.info("Model training scheduler started")
        
        # Run the scheduler
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

    def start(self):
        """Start the scheduler in a background thread."""
        self.scheduler_thread = threading.Thread(target=self.run_scheduler)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()
        logger.info("Training scheduler started in background thread")

    def trigger_retraining(self):
        """Trigger immediate model retraining."""
        thread = threading.Thread(target=self.train_job)
        thread.start()
        return {
            "status": "success",
            "message": "Model retraining started in background"
        } 