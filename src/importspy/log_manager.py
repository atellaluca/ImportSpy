"""
importspy.log_manager
======================

This module defines ImportSpy’s centralized logging system.

Logging is a critical part of ImportSpy: it tracks validation steps, configuration issues,  
execution context, and errors — all with enhanced formatting for debugging and traceability.

The `LogManager` ensures that all logs across ImportSpy are consistent and traceable to their source.  
It works in both **embedded validation** and **CLI validation**, enabling readable, structured output  
for developers, testers, and CI pipelines.
"""

import logging


class CustomFormatter(logging.Formatter):
    """
    Enhanced formatter for ImportSpy log messages.

    This formatter extends the default logging format by appending the exact
    filename, line number, and function name where each log was triggered.

    Format:
    -------
    [timestamp] [LEVEL] [logger name] 
    [caller: file, line, function] message

    Example:
    --------
    2024-02-24 14:30:12 [INFO] [my_logger] 
    [caller: example.py, line: 42, function: my_function] This is a log message.
    """

    LOG_FORMAT = (
        "%(asctime)s [%(levelname)s] [%(name)s] "
        "[caller: %(caller_file)s, line: %(caller_line)s, function: %(caller_function)s] "
        "%(message)s"
    )

    def __init__(self):
        """
        Initializes the formatter with the ImportSpy logging format.
        """
        super().__init__(self.LOG_FORMAT)

    def format(self, record):
        """
        Enriches the log record with caller information.

        Parameters:
        -----------
        record : logging.LogRecord
            The original log record to be formatted.

        Returns:
        --------
        str
            A fully formatted log message including file, line, and function context.
        """
        record.caller_file = record.pathname.split("/")[-1]
        record.caller_line = record.lineno
        record.caller_function = record.funcName
        return super().format(record)


class LogManager:
    """
    Centralized manager for all logging within ImportSpy.

    This class ensures:
    - Uniform formatting across all loggers
    - Avoidance of duplicate configuration
    - Consistent output in both CLI and embedded contexts

    Attributes:
    -----------
    default_level : int
        The current log level derived from the root logger.

    default_handler : logging.StreamHandler
        Default handler for logging output, using the `CustomFormatter`.

    configured : bool
        Whether the logging system has already been configured.
    """

    def __init__(self):
        """
        Sets up the default logging handler and format.

        Uses `CustomFormatter` and logs to standard output by default.
        """
        self.default_level = logging.getLogger().getEffectiveLevel()
        self.default_handler = logging.StreamHandler()
        self.default_handler.setFormatter(CustomFormatter())
        self.configured = False

    def configure(self, level: int = None, handlers: list = None):
        """
        Applies logging configuration globally.

        Prevents duplicate setup. This method should be called once per application.

        Parameters:
        -----------
        level : int, optional
            Log level (e.g., logging.DEBUG). Defaults to current system level.

        handlers : list of logging.Handler, optional
            Custom handlers to use. Falls back to `default_handler` if none provided.

        Raises:
        -------
        RuntimeError
            If logging is already configured.
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
        """
        Returns a named logger with ImportSpy's formatting applied.

        Ensures the logger is properly configured and ready for use.

        Parameters:
        -----------
        name : str
            The name of the logger (e.g., a module name).

        Returns:
        --------
        logging.Logger
            The initialized logger instance.
        """
        logger = logging.getLogger(name)
        if not logger.handlers:
            logger.addHandler(self.default_handler)
            logger.setLevel(logging.getLogger().getEffectiveLevel())
        return logger
