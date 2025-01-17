import logging

class CustomFormatter(logging.Formatter):
    """
    Custom formatter to include caller details in log messages.
    """
    LOG_FORMAT = (
        "%(asctime)s [%(levelname)s] [%(name)s] "
        "[caller: %(caller_file)s, line: %(caller_line)s, function: %(caller_function)s] "
        "%(message)s"
    )

    def __init__(self):
        super().__init__(self.LOG_FORMAT)

    def format(self, record):
        """
        Enrich the log record with caller information.
        """
        record.caller_file = record.pathname.split("/")[-1]  # Caller file
        record.caller_line = record.lineno                   # Caller line
        record.caller_function = record.funcName             # Caller function
        return super().format(record)


class LogManager:
    """
    LogManager for configuring and managing loggers in the ImportSpy framework.
    """

    def __init__(self):
        """
        Initialize the LogManager with default settings.

        By default, it uses the system's current logging level for configuration.
        """
        self.default_level = logging.getLogger().getEffectiveLevel()  # Use system-level configuration
        self.default_handler = logging.StreamHandler()
        self.default_handler.setFormatter(CustomFormatter())
        self.configured = False

    def configure(self, level=None, handlers=None):
        """
        Configure the logging system.

        Parameters:
        - level (int): Logging level to set globally. Defaults to the system's current level.
        - handlers (list): Optional list of custom handlers.
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

    def get_logger(self, name):
        """
        Get a logger configured with the custom formatter.

        Parameters:
        - name (str): Name of the logger.

        Returns:
        - logging.Logger: Configured logger instance.
        """
        logger = logging.getLogger(name)
        if not logger.handlers:  # Avoid duplicate handlers
            logger.addHandler(self.default_handler)
            logger.setLevel(logging.getLogger().getEffectiveLevel())  # Use current system logging level
        return logger
