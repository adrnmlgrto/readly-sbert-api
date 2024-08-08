import logging
import sys


class InMemoryLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.log_records = []

    def emit(self, record):
        self.log_records.append(self.format(record))

    def get_log_records(self):
        return self.log_records


def setup_logging() -> tuple[logging.Logger, InMemoryLogHandler]:
    """
    Set up logging configuration with a custom in-memory handler.
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

    # Create an in-memory log handler
    in_memory_handler = InMemoryLogHandler()
    in_memory_handler.setFormatter(formatter)

    # Add the handlers to the root logger
    root_logger.addHandler(console_handler)
    root_logger.addHandler(in_memory_handler)

    # Return a logger for the calling module and the in-memory handler
    return logging.getLogger(__name__), in_memory_handler
