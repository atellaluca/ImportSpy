from .config import Config

class Constants:
    
    KNOWN_ARCHITECTURES = [Config.ARCH_x86_64, 
                           Config.ARCH_AARCH64, 
                           Config.ARCH_ARM, 
                           Config.ARCH_ARM64, 
                           Config.ARCH_I386, 
                           Config.ARCH_PPC64, 
                           Config.ARCH_PPC64LE, 
                           Config.ARCH_S390X]

    SUPPORTED_OS = [Config.OS_WINDOWS,
                    Config.OS_LINUX, 
                    Config.OS_MACOS]

    SUPPORTED_PYTHON_IMPLEMENTATION = [Config.INTERPRETER_CPYTHON,
                                       Config.INTERPRETER_PYPY,
                                       Config.INTERPRETER_JYTHON,
                                       Config.INTERPRETER_IRON_PYTHON,
                                       Config.INTERPRETER_MICROPYTHON,
                                       Config.INTERPRETER_BRYTHON,
                                       Config.INTERPRETER_PYSTON,
                                       Config.INTERPRETER_GRAALPYTHON,
                                       Config.INTERPRETER_RUSTPYTHON,
                                       Config.INTERPRETER_NUITKA,
                                       Config.INTERPRETER_TRANSCRYPT]
    
    ATTRIBUTE_TYPES = [Config.CLASS_TYPE,
                       Config.INSTANCE_TYPE]

    DIE_ENVIRONMENT = "DIE - Default ImportSpy Environment"

    NAME = "name"
    VALUE = "value"

    CLASS_TYPE = Config.CLASS_TYPE
    INSTANCE_TYPE = Config.INSTANCE_TYPE