from importspy import (
    Spy
)

import logging

__version__ = None

caller_module = Spy().importspy(filepath="./spymodel.yml", log_level=logging.WARN)
caller_module.Foo().get_bar()