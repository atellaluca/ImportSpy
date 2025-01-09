class Constants:
    """
    A central repository for static definitions used throughout the ImportSpy package.

    This class defines known architecture constants and provides a standardized reference
    for supported system architectures. These constants are utilized to identify and handle
    platform-specific module requirements in ImportSpy.

    Attributes:
        KNOWN_ARCHITECTURES (list[str]): A list of all supported system architectures.
        ARCH_x86_64 (str): Identifier for the x86_64 architecture.
        ARCH_AARCH64 (str): Identifier for the aarch64 architecture.
        ARCH_ARM (str): Identifier for the ARM architecture.
        ARCH_ARM64 (str): Identifier for the ARM64 architecture.
        ARCH_I386 (str): Identifier for the i386 architecture.
        ARCH_PPC64 (str): Identifier for the PPC64 architecture.
        ARCH_PPC64LE (str): Identifier for the PPC64LE architecture.
        ARCH_S390X (str): Identifier for the S390X architecture.
    """
    
    KNOWN_ARCHITECTURES = ['x86_64', 'aarch64', 'arm', 'arm64', 'i386', 'ppc64', 'ppc64le', 's390x']

    ARCH_x86_64 = "x86_64"
    ARCH_AARCH64 = "aarch64"
    ARCH_ARM = "arm"
    ARCH_ARM64 = "arm64"
    ARCH_I386 = "i386"
    ARCH_PPC64 = "ppc64"
    ARCH_PPC64LE = "ppc64le"
    ARCH_S390X = "s390x"

    SUPPORTED_OS = ["windows", "linux", "darwin"]
    OS_WINDOWS = "windows"
    OS_LINUX = "linux"
    OS_MACOS = "darwin"

    SUPPORTED_PYTHON_IMPLEMENTATION = ["CPython", "PyPy", "Jython", "IronPython"]
    INTERPRETER_CPYTHON = "CPython"
    INTERPRETER_PYPY = "PyPy"
    INTERPRETER_JYTHON = "Jython"
    INTERPRETER_IRON_PYTHON = "IronPython"

    ATTRIBUTE_TYPES = ["class", "instance"]

    DIE_ENVIRONMENT = "DIE - Default ImportSpy Environment"