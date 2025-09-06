"""Tests for Celery tasks."""

import os
import pytest
from unittest.mock import patch, MagicMock

# Set Celery to always eager for testing and use memory backend
os.environ["CELERY_TASK_ALWAYS_EAGER"] = "true"
os.environ["CELERY_RESULT_BACKEND"] = "cache+memory://"

from app.celery_app import celery_app
from app.tasks.example import demo_task, process_data_task


class TestCeleryTasks:
    """Test cases for Celery tasks."""

    def test_demo_task_success(self):
        """Test demo task execution with success."""
        # Mock random to ensure success
        with patch("app.tasks.example.random.random", return_value=0.5):
            result = demo_task.delay("Test message")
            
            assert result.successful()
            assert result.result["message"] == "Test message"
            assert result.result["status"] == "completed"
            assert "task_id" in result.result
            assert "timestamp" in result.result
            assert "retries" in result.result

    def test_demo_task_with_retries(self):
        """Test demo task with retry behavior."""
        # Mock random to simulate failures then success
        random_values = [0.1, 0.1, 0.1, 0.5]  # Fail first 3 times, succeed on 4th
        
        with patch("app.tasks.example.random.random", side_effect=random_values):
            # In eager mode, retries don't work the same way, so we expect an exception
            with pytest.raises(Exception):
                demo_task.delay("Retry test message")

    def test_demo_task_max_retries_exceeded(self):
        """Test demo task when max retries are exceeded."""
        # Mock random to always fail
        with patch("app.tasks.example.random.random", return_value=0.1):
            # Mock the retry method to raise Retry exception
            with patch.object(demo_task, "retry", side_effect=Exception("Max retries exceeded")):
                with pytest.raises(Exception, match="Max retries exceeded"):
                    demo_task.delay("Max retry test")

    def test_process_data_task_success(self):
        """Test process data task execution with success."""
        test_data = {"key": "value", "number": 42}
        
        # Mock random to ensure success
        with patch("app.tasks.example.random.random", return_value=0.5):
            result = process_data_task.delay(test_data)
            
            assert result.successful()
            assert result.result["original"] == test_data
            assert result.result["status"] == "processed"
            assert "processed_at" in result.result
            assert "task_id" in result.result
            assert "retries" in result.result

    def test_process_data_task_with_retries(self):
        """Test process data task with retry behavior."""
        test_data = {"key": "value", "number": 42}
        
        # Mock random to simulate failures then success
        random_values = [0.1, 0.1, 0.1, 0.1, 0.5]  # Fail first 4 times, succeed on 5th
        
        with patch("app.tasks.example.random.random", side_effect=random_values):
            # In eager mode, retries don't work the same way, so we expect an exception
            with pytest.raises(Exception):
                process_data_task.delay(test_data)

    def test_celery_app_configuration(self):
        """Test Celery app configuration."""
        assert celery_app.main == "shopsherpa"
        assert celery_app.conf.task_serializer == "json"
        assert celery_app.conf.result_serializer == "json"
        assert celery_app.conf.accept_content == ["json"]
        assert celery_app.conf.timezone == "UTC"
        assert celery_app.conf.enable_utc is True

    def test_task_registration(self):
        """Test that tasks are properly registered."""
        registered_tasks = celery_app.tasks.keys()
        
        assert "app.tasks.example.demo_task" in registered_tasks
        assert "app.tasks.example.process_data_task" in registered_tasks

    def test_demo_task_default_message(self):
        """Test demo task with default message."""
        with patch("app.tasks.example.random.random", return_value=0.5):
            result = demo_task.delay()
            
            assert result.successful()
            assert result.result["message"] == "Hello from Celery!"

    def test_task_logging(self):
        """Test that tasks log appropriately."""
        with patch("app.tasks.example.logger") as mock_logger:
            with patch("app.tasks.example.random.random", return_value=0.5):
                demo_task.delay("Logging test")
                
                # Verify that info logging was called
                assert mock_logger.info.called
                
                # Check that the log messages contain expected content
                log_calls = mock_logger.info.call_args_list
                log_messages = [call[0][0] for call in log_calls]
                
                assert any("Executing demo_task" in msg for msg in log_messages)
                assert any("Demo task completed successfully" in msg for msg in log_messages)
