import logging
import sys


def setup_logging() -> logging.Logger:
    """
    Set up logging configuration with a custom formatter.

    This function configures the root logger with the following:
    - Sets the logging level to ERROR
    - Uses a custom formatter that includes timestamp, logger name,
      log level, filename, line number, and the log message
    - Outputs logs to the console (stdout)

    Returns:
        logging.Logger: A configured logger instance ready for use
        in the application.
    """
    # Create a custom formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - '
        '%(filename)s:%(lineno)d - %(message)s'
    )

    # Configure the root logger
    logging.basicConfig(level=logging.ERROR, handlers=[])
    root_logger = logging.getLogger()

    # Create a console handler and set the formatter
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # Add the console handler to the root logger
    root_logger.addHandler(console_handler)

    # Return a logger for the calling module
    return logging.getLogger(__name__)
