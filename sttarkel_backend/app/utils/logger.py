"""
Logging utility for SttarkelTool backend.
Provides centralized logging configuration and utilities.
"""

import logging
import sys
from typing import Optional
from datetime import datetime
from app.config import settings


def get_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    """
    Get a configured logger instance.
    
    Args:
        name: Logger name (usually __name__)
        level: Logging level (optional, defaults to INFO)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Set logging level
    if level is None:
        level = logging.DEBUG if settings.debug else logging.INFO
    logger.setLevel(level)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    return logger


def log_function_call(func_name: str, args: dict = None, kwargs: dict = None):
    """
    Decorator to log function calls.
    
    Args:
        func_name: Name of the function being called
        args: Function arguments
        kwargs: Function keyword arguments
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = get_logger(func.__module__)
            logger.debug(f"Calling {func_name} with args={args}, kwargs={kwargs}")
            try:
                result = func(*args, **kwargs)
                logger.debug(f"{func_name} completed successfully")
                return result
            except Exception as e:
                logger.error(f"{func_name} failed with error: {str(e)}")
                raise
        return wrapper
    return decorator


def log_performance(func_name: str):
    """
    Decorator to log function performance.
    
    Args:
        func_name: Name of the function being timed
    """
    def decorator(func):
        async def async_wrapper(*args, **kwargs):
            logger = get_logger(func.__module__)
            start_time = datetime.now()
            try:
                result = await func(*args, **kwargs)
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                logger.info(f"{func_name} completed in {duration:.3f} seconds")
                return result
            except Exception as e:
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                logger.error(f"{func_name} failed after {duration:.3f} seconds: {str(e)}")
                raise
        
        def sync_wrapper(*args, **kwargs):
            logger = get_logger(func.__module__)
            start_time = datetime.now()
            try:
                result = func(*args, **kwargs)
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                logger.info(f"{func_name} completed in {duration:.3f} seconds")
                return result
            except Exception as e:
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                logger.error(f"{func_name} failed after {duration:.3f} seconds: {str(e)}")
                raise
        
        # Return appropriate wrapper based on function type
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


class RequestLogger:
    """Middleware for logging HTTP requests."""
    
    def __init__(self, app):
        self.app = app
        self.logger = get_logger("request_logger")
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            start_time = datetime.now()
            
            # Log request
            self.logger.info(f"Request: {scope['method']} {scope['path']}")
            
            # Process request
            await self.app(scope, receive, send)
            
            # Log response time
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            self.logger.info(f"Response: {scope['method']} {scope['path']} - {duration:.3f}s")
        else:
            await self.app(scope, receive, send)


def log_error(error: Exception, context: str = None):
    """
    Log an error with context.
    
    Args:
        error: The exception that occurred
        context: Additional context about where the error occurred
    """
    logger = get_logger("error_logger")
    error_msg = f"Error in {context}: {str(error)}" if context else str(error)
    logger.error(error_msg, exc_info=True)


def log_info(message: str, context: str = None):
    """
    Log an info message with context.
    
    Args:
        message: The message to log
        context: Additional context
    """
    logger = get_logger("info_logger")
    info_msg = f"[{context}] {message}" if context else message
    logger.info(info_msg)


def log_warning(message: str, context: str = None):
    """
    Log a warning message with context.
    
    Args:
        message: The warning message
        context: Additional context
    """
    logger = get_logger("warning_logger")
    warning_msg = f"[{context}] {message}" if context else message
    logger.warning(warning_msg)


def log_debug(message: str, context: str = None):
    """
    Log a debug message with context.
    
    Args:
        message: The debug message
        context: Additional context
    """
    logger = get_logger("debug_logger")
    debug_msg = f"[{context}] {message}" if context else message
    logger.debug(debug_msg) 