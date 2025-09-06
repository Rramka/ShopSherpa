"""Celery application configuration."""

import logging
import os
from celery import Celery
from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Celery instance
# Use memory backend and broker for testing when CELERY_TASK_ALWAYS_EAGER is set
result_backend = settings.celery_result_backend
broker_url = settings.celery_broker_url
if os.environ.get("CELERY_TASK_ALWAYS_EAGER") == "true":
    result_backend = "cache+memory://"
    broker_url = "memory://"

celery_app = Celery(
    "shopsherpa",
    broker=broker_url,
    backend=result_backend,
    include=["app.tasks.example"],
)

# Celery configuration
celery_app.conf.update(
    task_serializer=settings.celery_task_serializer,
    result_serializer=settings.celery_result_serializer,
    accept_content=settings.celery_accept_content,
    timezone=settings.celery_timezone,
    enable_utc=settings.celery_enable_utc,
    # Task execution settings
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    # Retry settings
    task_acks_late=True,
    worker_disable_rate_limits=False,
    # Logging
    worker_log_format="[%(asctime)s: %(levelname)s/%(processName)s] %(message)s",
    worker_task_log_format="[%(asctime)s: %(levelname)s/%(processName)s][%(task_name)s(%(task_id)s)] %(message)s",
)

# Apply test configuration if CELERY_TASK_ALWAYS_EAGER is set
if os.environ.get("CELERY_TASK_ALWAYS_EAGER") == "true":
    celery_app.conf.update(
        task_always_eager=True,
        task_eager_propagates=True,
    )

# Configure JSON logging for retries/backoff
class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging."""
    
    def format(self, record):
        import json
        log_entry = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add Celery-specific fields
        if hasattr(record, "task_id"):
            log_entry["task_id"] = record.task_id
        if hasattr(record, "task_name"):
            log_entry["task_name"] = record.task_name
        if hasattr(record, "retries"):
            log_entry["retries"] = record.retries
        if hasattr(record, "backoff"):
            log_entry["backoff"] = record.backoff
            
        return json.dumps(log_entry)

# Apply JSON formatter to Celery logger
celery_logger = logging.getLogger("celery")
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
celery_logger.addHandler(handler)
celery_logger.setLevel(logging.INFO)

logger.info("Celery app configured successfully")
