"""Example Celery tasks with retry functionality."""

import logging
import random
import time
from typing import Any, Dict

from celery import Task
from celery.exceptions import Retry
from app.celery_app import celery_app

logger = logging.getLogger(__name__)


class CallbackTask(Task):
    """Base task class with retry logging."""
    
    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """Log retry attempts with backoff information."""
        logger.info(
            f"Task {self.name} retry {self.request.retries + 1}/{self.max_retries}",
            extra={
                "task_id": task_id,
                "task_name": self.name,
                "retries": self.request.retries + 1,
                "max_retries": self.max_retries,
                "backoff": self.default_retry_delay * (2 ** self.request.retries),
                "exception": str(exc),
            }
        )
        super().on_retry(exc, task_id, args, kwargs, einfo)
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Log task failures."""
        logger.error(
            f"Task {self.name} failed after {self.request.retries} retries",
            extra={
                "task_id": task_id,
                "task_name": self.name,
                "retries": self.request.retries,
                "exception": str(exc),
            }
        )
        super().on_failure(exc, task_id, args, kwargs, einfo)
    
    def on_success(self, retval, task_id, args, kwargs):
        """Log successful task completion."""
        logger.info(
            f"Task {self.name} completed successfully",
            extra={
                "task_id": task_id,
                "task_name": self.name,
                "retries": self.request.retries,
            }
        )
        super().on_success(retval, task_id, args, kwargs)


@celery_app.task(
    bind=True,
    base=CallbackTask,
    max_retries=3,
    default_retry_delay=1,
    retry_backoff=True,
    retry_backoff_max=60,
    retry_jitter=True,
)
def demo_task(self: CallbackTask, message: str = "Hello from Celery!") -> Dict[str, Any]:
    """
    Demo task that demonstrates retry functionality.
    
    This task randomly fails to demonstrate retry behavior.
    After 3 retries, it will succeed.
    
    Args:
        message: A message to include in the result
        
    Returns:
        Dict containing task result information
        
    Raises:
        Retry: When the task should be retried
    """
    logger.info(f"Executing demo_task with message: {message}")
    
    # Simulate some work
    time.sleep(0.1)
    
    # Randomly fail to demonstrate retries (30% chance)
    if random.random() < 0.3 and self.request.retries < 2:
        logger.warning(f"Demo task failed on attempt {self.request.retries + 1}")
        raise self.retry(
            countdown=self.default_retry_delay * (2 ** self.request.retries),
            exc=Exception(f"Simulated failure on attempt {self.request.retries + 1}")
        )
    
    # Success case
    result = {
        "message": message,
        "task_id": self.request.id,
        "retries": self.request.retries,
        "timestamp": time.time(),
        "status": "completed",
    }
    
    logger.info(f"Demo task completed successfully: {result}")
    return result


@celery_app.task(
    bind=True,
    base=CallbackTask,
    max_retries=5,
    default_retry_delay=2,
    retry_backoff=True,
    retry_backoff_max=120,
    retry_jitter=True,
)
def process_data_task(self: CallbackTask, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Example task for processing data with retry logic.
    
    Args:
        data: Dictionary containing data to process
        
    Returns:
        Dict containing processed data and metadata
    """
    logger.info(f"Processing data: {data}")
    
    # Simulate processing time
    time.sleep(0.2)
    
    # Simulate occasional failures (20% chance)
    if random.random() < 0.2 and self.request.retries < 4:
        logger.warning(f"Data processing failed on attempt {self.request.retries + 1}")
        raise self.retry(
            countdown=self.default_retry_delay * (2 ** self.request.retries),
            exc=Exception(f"Data processing failed on attempt {self.request.retries + 1}")
        )
    
    # Process the data
    processed_data = {
        "original": data,
        "processed_at": time.time(),
        "task_id": self.request.id,
        "retries": self.request.retries,
        "status": "processed",
    }
    
    logger.info(f"Data processing completed: {processed_data}")
    return processed_data
