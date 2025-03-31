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

    This is especially useful in distributed architectures, plugin-based systems, 
    or debugging deeply nested calls during module inspection.

    Format:
    -------
    ``[timestamp] [LEVEL] [logger name] [caller: file, line, function] message``

    Example:
    --------
    .. code-block:: text

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
        Adds caller details to the log record.

        Enhances logs with:
        - Filename where the log was triggered
        - Line number
        - Function name

        Parameters:
        -----------
        record : logging.LogRecord
            The original log event.

        Returns:
        --------
        str
            The enriched, formatted log message.
        """
        record.caller_file = record.pathname.split("/")[-1]
        record.caller_line = record.lineno
        record.caller_function = record.funcName
        return super().format(record)


class LogManager:
    """
    Centralized manager for all logging within ImportSpy.

    This class ensures that:
    - All loggers use the same format (`CustomFormatter`)
    - Logging is only configured once to avoid duplication
    - Each component of the framework can retrieve its own scoped logger

    Whether ImportSpy runs embedded inside another module or as a CLI tool,  
    the `LogManager` ensures that log output is clean, traceable, and standardized.

    Attributes:
    -----------
    default_level : int
        The system's current log level at the time of instantiation.

    default_handler : logging.StreamHandler
        Default output handler using `CustomFormatter`.

    configured : bool
        Indicates whether global logging has already been configured.

    Methods:
    --------
    - `configure(level, handlers)`: Applies global settings to the root logger.
    - `get_logger(name)`: Retrieves a logger with consistent formatting and context.
    """

    def __init__(self):
        """
        Sets up default logging options.

        The default handler uses ImportSpy’s `CustomFormatter` and logs to `stdout`.
        Logging is deferred until explicitly configured.
        """
        self.default_level = logging.getLogger().getEffectiveLevel()
        self.default_handler = logging.StreamHandler()
        self.default_handler.setFormatter(CustomFormatter())
        self.configured = False

    def configure(self, level: int = None, handlers: list = None):
        """
        Configures the global logging system.

        This method attaches handlers to the root logger and sets the global level.  
        It must be called only once to avoid duplicate logs or handler conflicts.

        Parameters:
        -----------
        level : int, optional
            Desired log level (e.g., `logging.DEBUG` or `logging.INFO`).  
            Defaults to the system’s current level.

        handlers : list of logging.Handler, optional
            List of custom handlers to attach. If omitted, uses the default stream handler.

        Raises:
        -------
        RuntimeError
            If logging has already been configured elsewhere in the application.

        Example:
        --------
        .. code-block:: python

            LogManager().configure(level=logging.DEBUG)
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
        Retrieves a scoped logger configured with ImportSpy’s formatting.

        This logger is safe to use across modules and plugins.  
        It ensures no duplicate handlers and maintains the current log level.

        Parameters:
        -----------
        name : str
            Name of the logger (typically `__name__` or class name).

        Returns:
        --------
        logging.Logger
            A configured logger ready for use.

        Example:
        --------
        .. code-block:: python

            logger = LogManager().get_logger("my_module")
            logger.info("Validation complete.")
        """
        logger = logging.getLogger(name)
        if not logger.handlers:
            logger.addHandler(self.default_handler)
            logger.setLevel(logging.getLogger().getEffectiveLevel())
        return logger
