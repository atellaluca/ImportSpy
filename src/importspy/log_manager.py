"""importspy.log_manager

Centralized logging system for ImportSpy.

This module defines logging utilities that ensure consistent formatting,
traceability, and developer-friendly output across both embedded and CLI modes.
The `LogManager` provides a global configuration entry point for logging,
while `CustomFormatter` enhances each message with context such as file name,
line number, and function.

Used in ImportSpy to provide high-fidelity logs during validation steps,
contract resolution, and runtime introspection.
"""

import logging


class CustomFormatter(logging.Formatter):
    """Enhanced formatter for ImportSpy log messages.

    Adds contextual metadata (file, line, function) to each log entry, improving
    traceability across CLI execution and embedded imports.

    Format:
        "[timestamp] LEVEL logger name"
        "[caller: file, line, function] message"

    Example:
        2025-08-07 14:30:12 INFO importspy.module
        caller: loader.py, line: 42, function: validate_import
        Validation passed.
    """

    LOG_FORMAT = (
        "%(asctime)s [%(levelname)s] [%(name)s] "
        "[caller: %(caller_file)s, line: %(caller_line)s, function: %(caller_function)s] "
        "%(message)s"
    )

    def __init__(self):
        """Initialize the formatter with ImportSpy's extended log format."""
        super().__init__(self.LOG_FORMAT)

    def format(self, record) -> str:
        """Format the log record with caller information.

        Adds custom attributes to the `LogRecord` for file name, line number,
        and function name.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: Formatted log message string.
        """
        record.caller_file = record.pathname.split("/")[-1]
        record.caller_line = record.lineno
        record.caller_function = record.funcName
        return super().format(record)


class LogManager:
    """Centralized manager for logging configuration in ImportSpy.

    Ensures that all logs share a consistent format and output behavior,
    avoiding duplicate configuration across modules. Designed for both
    embedded validation flows and CLI analysis.

    Attributes:
        default_level (int): Default log level from the root logger.
        default_handler (logging.StreamHandler): Stream handler with ImportSpy formatting.
        configured (bool): Whether the logger has already been initialized.
    """

    def __init__(self):
        """Initialize the default logging handler and formatter."""
        self.default_level = logging.getLogger().getEffectiveLevel()
        self.default_handler = logging.StreamHandler()
        self.default_handler.setFormatter(CustomFormatter())
        self.configured = False

    def configure(self, level: int = None, handlers: list = None):
        """Apply logging configuration globally.

        Should be called once per execution to avoid duplicated handlers.
        Adds provided handlers or defaults to the built-in stream handler.

        Args:
            level (int, optional): Logging level (e.g., logging.DEBUG). Defaults to current level.
            handlers (list[logging.Handler], optional): Custom logging handlers.

        Raises:
            RuntimeError: If configuration is attempted more than once.
        """
        if self.configured:
            raise RuntimeError("LogManager has already been configured.")

        level = level or self.default_level

        if handlers:
            for handler in handlers:
                logging.getLogger().addHandler(handler)
        else:
            logging.getLogger().addHandler(self.default_handler)

        logging.getLogger().setLevel(level)
        self.configured = True

    def get_logger(self, name: str) -> logging.Logger:
        """Return a named logger configured with ImportSpy's formatter.

        Ensures consistent behavior across all log invocations. If the logger
        does not yet have handlers, it assigns the default handler.

        Args:
            name (str): Name of the logger (typically a module or subpackage name).

        Returns:
            logging.Logger: A logger instance ready for use.
        """
        logger = logging.getLogger(name)
        if not logger.handlers:
            logger.addHandler(self.default_handler)
            logger.setLevel(logging.getLogger().getEffectiveLevel())
        return logger
