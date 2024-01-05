# logger_setup.py
import logging
import sys

def setup_logger():
    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Set the logging level

    # Create a file handler
    file_handler = logging.FileHandler('app.log')
    file_handler.setLevel(logging.DEBUG)  # Set the logging level

    # Create a stream handler for stdout
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)  # Set the logging level

    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')

    # Add the formatter to the handlers
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


