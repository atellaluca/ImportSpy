import logging

class CustomFormatter(logging.Formatter):
    """
    Custom log formatter that enhances log messages with caller details.

    This formatter extends the standard logging format by appending information 
    about the calling file, line number, and function name.

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
        Initializes the `CustomFormatter` with the predefined log format.
        """
        super().__init__(self.LOG_FORMAT)

    def format(self, record):
        """
        Formats the log record by adding caller details.

        Modifies the `record` object to include:
        - `caller_file`: The filename where the log was generated.
        - `caller_line`: The line number in the source file.
        - `caller_function`: The function from which the log originated.

        Parameters:
        -----------
        record : logging.LogRecord
            The log record instance containing log details.

        Returns:
        --------
        str
            The formatted log message.
        """
        record.caller_file = record.pathname.split("/")[-1]
        record.caller_line = record.lineno
        record.caller_function = record.funcName
        return super().format(record)


class LogManager:
    """
    Log manager for configuring and retrieving loggers with a standardized format.

    The `LogManager` ensures consistent logging across the ImportSpy framework. 
    It applies a custom formatter to enhance log messages with caller details and 
    prevents duplicate log handlers.

    Attributes:
    -----------
    default_level : int
        The system's current logging level (e.g., `logging.DEBUG`, `logging.INFO`).
    default_handler : logging.StreamHandler
        Default logging handler using `CustomFormatter`.
    configured : bool
        Flag indicating whether logging has already been configured.

    Methods:
    --------
    - `configure(level=None, handlers=None)`: Sets the logging level and handlers.
    - `get_logger(name)`: Returns a logger instance with the custom formatter.
    """

    def __init__(self):
        """
        Initializes the `LogManager` with default logging settings.

        - Uses the system's current logging level.
        - Configures a default stream handler with `CustomFormatter`.
        """
        self.default_level = logging.getLogger().getEffectiveLevel()
        self.default_handler = logging.StreamHandler()
        self.default_handler.setFormatter(CustomFormatter())
        self.configured = False

    def configure(self, level: int = None, handlers: list = None):
        """
        Configures the logging system globally.

        This method sets the logging level and attaches handlers to the root logger.
        If handlers are not provided, it applies the default stream handler.

        Parameters:
        -----------
        level : int, optional
            Logging level to set globally (e.g., `logging.DEBUG`, `logging.INFO`).
            If not specified, it defaults to the system's current logging level.

        handlers : list of logging.Handler, optional
            A list of custom logging handlers. If not provided, the default 
            stream handler is used.

        Raises:
        -------
        RuntimeError
            If an attempt is made to reconfigure logging after it has already been set.

        Example:
        --------
        .. code-block:: python

            log_manager = LogManager()
            log_manager.configure(level=logging.DEBUG)

        Notes:
        ------
        - This method ensures logging is configured only once to prevent 
          duplicate handlers or inconsistent log levels.
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
        Retrieves a logger instance with the configured settings.

        This method ensures that the logger:
        - Uses the `CustomFormatter` for enhanced log messages.
        - Avoids duplicate handlers.
        - Adheres to the globally configured logging level.

        Parameters:
        -----------
        name : str
            The name of the logger (typically the module or class name).

        Returns:
        --------
        logging.Logger
            A logger instance configured with `CustomFormatter`.

        Example:
        --------
        .. code-block:: python

            log_manager = LogManager()
            logger = log_manager.get_logger("importspy")
            logger.info("This is a log message.")

        Notes:
        ------
        - If the logger already has handlers, it does not attach new ones to 
          prevent duplicate log outputs.
        """
        logger = logging.getLogger(name)
        if not logger.handlers:
            logger.addHandler(self.default_handler)
            logger.setLevel(logging.getLogger().getEffectiveLevel())
        return logger
