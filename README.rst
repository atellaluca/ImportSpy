.. image:: https://static.pepy.tech/badge/importspy
   :target: https://pepy.tech/project/importspy

.. image:: https://img.shields.io/github/actions/workflow/status/atellaluca/ImportSpy/python-package.yml?style=flat-square
   :target: https://github.com/atellaluca/ImportSpy/actions/workflows/python-package.yml

.. image:: https://img.shields.io/github/license/atellaluca/ImportSpy?style=flat-square
   :target: https://github.com/atellaluca/ImportSpy/blob/master/LICENSE

ImportSpy
=========

.. image:: https://raw.githubusercontent.com/atellaluca/ImportSpy/refs/heads/main/assets/ImportSpy.png
   :width: 830
   :alt: ImportSpy Image

Overview 🌌
===========

In the modern era of software development, ensuring **reliability**, **scalability**, and **security** has become a cornerstone of successful projects. Runtime environment management and module validation are critical processes in achieving these goals. **ImportSpy** is a cutting-edge Python library designed to provide developers with unparalleled control over how their code interacts with external modules, making it a vital tool for building robust and compliant systems.

With its innovative approach, ImportSpy leverages advanced reflection techniques, declarative validation models, and structured abstractions to empower developers. It ensures that their code operates predictably across diverse environments, all while maintaining a high standard of security and adaptability.

**Theoretical Underpinnings**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
At its core, ImportSpy is rooted in sound principles of software development and computer science:

- **Reflection and Introspection**:
  ImportSpy utilizes Python's dynamic capabilities to analyze the current runtime environment in real time. It extracts details such as the operating system, processor architecture, Python version, and implementation, providing a complete snapshot of the execution context.

- **Declarative Validation**:
  Using the `SpyModel`, developers can define the exact structure and behavior they expect from external modules and runtime environments. This approach shifts the focus from reactive debugging to proactive validation.

- **Granular Abstraction**:
  ImportSpy models the entire execution stack—from deployments and runtimes to individual class attributes and function arguments. This level of detail enables fine-grained control over validation processes.

- **Modern Software Practices**:
  By incorporating Python's type annotations, ImportSpy promotes robust and adaptable validation for all components. This aligns with modern software development trends and improves code maintainability and readability.

Why ImportSpy? 🛠️
=================

ImportSpy stands out in the Python ecosystem through its unique combination of features and benefits:

.. list-table::
   :widths: 10 40 50
   :header-rows: 1

   * -
     - **Feature**
     - **Description**
   * - ✅
     - **Cross-Platform Compatibility**
     - Validate your code's usage across diverse operating systems, processor architectures, and Python implementations with ease.
   * - ✅
     - **Security by Design**
     - Prevent unauthorized or malicious usage through rigorous runtime validations that safeguard your codebase.
   * - ✅
     - **Dynamic Adjustments**
     - Adapt to varying runtime conditions with precision, ensuring compatibility and seamless integration in dynamic environments.
   * - ✅
     - **Actionable Feedback**
     - Deliver comprehensive and meaningful error messages, enabling developers to quickly identify and resolve inconsistencies.

Key Features 🛠️
================

**Proactive Import Validation**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ImportSpy ensures that external modules using your code adhere to predefined structures and behaviors, eliminating runtime inconsistencies and enhancing reliability.

- **Define Expectations**: Specify the components (functions, variables, classes) that external modules must include.
- **Validate Modern Practices**: Incorporate type annotations to enforce stricter and more adaptable programming styles.

**Cross-Platform Compatibility**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ImportSpy ensures seamless operation across a range of environments, including:

- **Processor Architectures**: Validate compatibility with `x86_64`, `ARM64`, and other architectures.
- **Operating Systems**: Support environments like `Linux`, `Windows`, and `macOS`.
- **Python Implementations and Versions**: Ensure compatibility with `CPython`, `PyPy`, and others, while addressing differences between Python 3.8, 3.10, and beyond.

**Dynamic Metadata Recognition**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ImportSpy dynamically analyzes and extracts metadata from the runtime environment, enabling informed decision-making. This includes:

- **Function Details**: Extract argument names, annotations, and return types.
- **Class Hierarchies**: Identify inheritance patterns and attributes.
- **Actionable Insights**: Provide a clear understanding of runtime module structures.

**Cloud-Native and IoT Validation**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In distributed and edge computing, consistency across environments is essential. ImportSpy ensures:

- **Edge Device Validation**: Verify IoT plugins for specific hardware architectures and OS environments.
- **Cloud Deployment Consistency**: Validate Kubernetes and Docker deployments against runtime expectations.

**Enhanced Security**
~~~~~~~~~~~~~~~~~~~~~

With a strong focus on security, ImportSpy provides:

- **Environment Variable Validation**: Check for critical configurations, such as `AUTH_TOKEN` or `ENCRYPTION_KEY`.
- **Structural Safeguards**: Enforce strict module structures to prevent misuse or misconfiguration.
- **Error Messaging**: Provide actionable warnings and errors that guide developers to address potential vulnerabilities.

ImportSpy isn’t just another library—it’s a paradigm shift in how Python developers manage runtime environments and validate code interactions. By bridging the gap between flexibility and control, ImportSpy makes your code more reliable, secure, and adaptable to the complexities of modern software development.

Detailed Example: IoT Plugin Validation 🌐
==========================================

In the rapidly growing world of IoT, ensuring compatibility and reliability across diverse hardware and software environments is a critical challenge. ImportSpy simplifies this by providing a declarative framework for validating runtime environments and module compliance.

**Scenario**:
Imagine a smart home hub that integrates third-party sensor plugins to monitor temperature, humidity, and motion. These plugins must comply with specific requirements based on the hub's hardware, operating system, and Python runtime.

**Objective**:
Use ImportSpy to validate IoT plugins, ensuring compatibility with the smart home hub's architecture (`ARM64`), operating system (`Linux`), and Python runtime (`3.8`).

**Developer-Defined SpyModel**:
The `SpyModel` defines the required structure for IoT plugins, including runtime configurations, expected classes, attributes, and methods.

.. code-block:: python

    from importspy.models import SpyModel, Deployment, Runtime, System, Python, Class, Attribute, Function, Argument
    from importspy.constants import Config

    class IoTPluginSpy(SpyModel):
        deployments: List[Deployment] = [
            Deployment(
                runtimes=[
                    Runtime(
                        arch=Config.ARCH_ARM64,
                        systems=[
                            System(
                                os=Config.OS_LINUX,
                                pythons=[
                                    Python(
                                        version="3.8",
                                        interpreter=Config.INTERPRETER_CPYTHON,
                                        modules=[]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
        classes: List[Class] = [
            Class(
                name="SensorPlugin",
                attributes=[
                    Attribute(type=Config.CLASS_TYPE, name="plugin_name", value="TemperatureSensor"),
                    Attribute(type=Config.INSTANCE_TYPE, name="sensor_id", value=None)
                ],
                methods=[
                    Function(
                        name="initialize",
                        arguments=[
                            Argument(name="self")
                        ]
                    ),
                    Function(
                        name="send_data",
                        arguments=[
                            Argument(name="self"),
                            Argument(name="data", annotation="dict")
                        ]
                    )
                ]
            )
        ]

**Compliant IoT Plugin Example**:
Here’s a compliant implementation of an IoT plugin that adheres to the defined `SpyModel`.

.. code-block:: python

    class SensorPlugin:
        plugin_name = "TemperatureSensor"

        def __init__(self):
            self.sensor_id = None

        def initialize(self):
            print("Sensor initialized.")

        def send_data(self, data: dict):
            print(f"Data sent: {data}")

**Non-Compliant IoT Plugin Example**:
This implementation is non-compliant due to missing attributes and an incorrect method signature.

.. code-block:: python

    class SensorPlugin:
        def __init__(self):
            pass  # Missing required attributes

        def send_data(self, temperature: float):
            print(f"Temperature: {temperature}")  # Incorrect method signature

**Validation and Adaptation**: When a non-compliant plugin is detected, ImportSpy provides actionable feedback, allowing developers to adapt their implementations.

**Example Feedback**:

- Missing attribute: `plugin_name` in class `SensorPlugin`.
- Method signature mismatch for `send_data`. Expected `send_data(self, data: dict)`, found `send_data(self, temperature: float)`.

**Revised Plugin**:

Here’s the corrected implementation of the plugin based on ImportSpy’s feedback.

.. code-block:: python

    class SensorPlugin:
        plugin_name = "TemperatureSensor"

        def __init__(self):
            self.sensor_id = None

        def initialize(self):
            print("Sensor initialized.")

        def send_data(self, data: dict):
            print(f"Data sent: {data}")

**Conclusion**:
ImportSpy ensures that IoT plugins are validated against the defined requirements, improving reliability and reducing integration issues. By leveraging ImportSpy’s reflective capabilities, developers can confidently integrate third-party modules into IoT ecosystems, ensuring consistent performance across all supported environments.

Use Cases 🖐️
============

**ImportSpy** provides innovative solutions for real-world challenges in software development, ensuring robust, secure, and adaptive applications.

.. list-table::
   :widths: 25 35 40
   :header-rows: 1

   * - **Use Case**
     - **Problem**
     - **Solution**
   * - **Library Compliance** 📚
     - Third-party plugins or libraries may lack required functions or inconsistent structures, causing runtime errors.
     - ImportSpy enforces compliance by:
       - Validating **mandatory functions** like `initialize_plugin`.
       - Ensuring presence of **critical environment variables**, such as `API_KEY` or `PLUGIN_ID`.
   * - **Environment-Specific Behavior** 🌍
     - Variations across processor architectures, operating systems, and Python versions lead to subtle bugs.
     - ImportSpy dynamically validates:
       - **Architectures**: `x86_64`, `ARM64`.
       - **Operating Systems**: `Linux`, `Windows`, `macOS`.
       - **Python Versions**: `3.8`, `3.10` (e.g., `CPython`, `PyPy`).
   * - **Security Enforcement** 🔒
     - Misconfigured cryptographic settings or missing secure API integrations can compromise application security.
     - ImportSpy ensures:
       - Validation of critical variables, e.g., `AUTH_TOKEN` or `ENCRYPTION_KEY`.
       - Rejection of non-compliant modules with actionable feedback.
   * - **Debugging & Issue Resolution** 🐞
     - Integration failures are often silent, making root cause analysis time-consuming and difficult.
     - ImportSpy provides detailed error messages to:
       - Identify missing variables (e.g., `CACHE_HOST`).
       - Detect structural inconsistencies in functions and classes.
   * - **Cloud-Native Validation** ☁️
     - Deployment inconsistencies in Kubernetes clusters or Docker containers cause unexpected failures.
     - ImportSpy validates:
       - Pre-deployment configurations for consistency.
       - Critical settings like `CACHE_SIZE` or `CONNECTION_LIMIT` across all nodes.
   * - **IoT Device Integration** 🌐
     - Standardizing integrations across diverse IoT hardware and software is a significant challenge.
     - ImportSpy ensures:
       - Plugins comply with specific architectures (e.g., `ARM64`) and operating systems (e.g., `Linux`).
       - Required methods like `initialize` and `send_data` are implemented correctly.

Technical Overview 🔬
=====================

Delve into the inner workings of ImportSpy and uncover the technical foundations that make it a powerful tool for runtime validation and module compliance.

Core Mechanism 🔬
=================

At the heart of **ImportSpy** lies a sophisticated and robust **two-phase validation process**, meticulously designed to ensure compatibility, reliability, and compliance across diverse runtime environments. This mechanism empowers developers to maintain full control over their code’s behavior in various contexts.

Developer-Defined SpyModel
~~~~~~~~~~~~~~~~~~~~~~~~~~~
The cornerstone of ImportSpy's functionality is the `SpyModel`, a highly customizable blueprint that defines the expected behaviors and structures for each deployment scenario. This declarative model allows developers to predefine critical aspects of their runtime environment:

- **Processor Architectures**: Enforce compatibility with specific architectures such as `x86_64` or `ARM64`.
- **Operating Systems**: Support a wide range of platforms including `Linux`, `macOS`, and `Windows`.
- **Python Runtimes**: Specify compatible Python versions (`3.8`, `3.10`, etc.) and implementations (`CPython`, `PyPy`).
- **Module Structures**: Define the required structure of modules, including:

  - **Functions**: Expected names, argument specifications, and return types.
  - **Classes**: Mandatory attributes, methods, and inheritance hierarchies.
  - **Variables**: Global and local variables with precise annotations.

By defining these rules upfront, developers can shift from reactive debugging to proactive validation, minimizing integration errors and ensuring consistent behavior across environments.

Runtime SpyModel Creation
~~~~~~~~~~~~~~~~~~~~~~~~~~
During execution, ImportSpy dynamically constructs a `SpyModel` representing the current runtime environment. This process leverages Python's introspective capabilities and advanced analysis techniques:

- **Reflection**: Extracts runtime details about functions, classes, variables, and their relationships within the module.
- **Introspection**: Captures key system-level properties, including:
  - Operating System and Architecture (e.g., `Linux`, `ARM64`).
  - Python implementation and version (e.g., `CPython 3.10`).
- **Dynamic Analysis**: Builds a detailed representation of the runtime state, mapping it to the predefined expectations.

Validation Process
~~~~~~~~~~~~~~~~~~
The validation process is where the magic happens. The dynamically generated `SpyModel` is compared against the developer-defined model to identify discrepancies and ensure compliance. This comparison involves three core checks:

1. **Structural Comparison**:
   - Validates that required classes, methods, and variables are present and properly structured.
   - Ensures adherence to declared hierarchies and relationships.

2. **Semantic Validation**:
   - Verifies argument specifications, return types, and type annotations.
   - Checks alignment with Python’s type hinting for modern programming practices.

3. **Environment Checks**:

   - Confirms the runtime environment meets all defined constraints, including:

     - System configurations (e.g., environment variables like `AUTH_TOKEN`).
     - Compatibility with the specified architecture and Python runtime.

Actionable Feedback 📋
~~~~~~~~~~~~~~~~~~~~~~
When inconsistencies are detected, ImportSpy provides **clear, actionable error messages**. These messages help developers pinpoint the root cause of issues and make precise adjustments. Examples include:

- `Missing class: 'UserManager'. Ensure it is defined in the module 'user_module'.`
- `Annotation mismatch for method 'process_data'. Expected return type 'List[str]', found 'str'.`
- `Invalid architecture 'arm64'. Supported architectures are: ['x86_64', 'aarch64'].`

By combining proactive validation with actionable insights, ImportSpy equips developers with the tools they need to build resilient, adaptable, and compliant software.

Summary
~~~~~~~
The **Core Mechanism** of ImportSpy bridges the gap between flexibility and control, enabling developers to confidently deploy code across diverse environments. From defining robust validation rules to dynamically analyzing runtime environments, ImportSpy delivers a comprehensive solution for ensuring runtime integrity and modular reliability.


Data Structures and Relationships 📊
=====================================

**ImportSpy** provides a comprehensive model of the entire execution stack, creating a hierarchical structure that abstracts components and their relationships. This modular design ensures precise validation across every level of the software stack.

Deployment 🌍
=============
A **Deployment** is a high-level abstraction that encompasses multiple runtime environments. It enables validation across diverse scenarios:

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - **Use Case**
     - **Description**
   * - **Edge Devices**
     - IoT sensors or gateways with specific hardware constraints.
   * - **CI/CD Pipelines**
     - Ensuring consistent configurations for automated workflows.
   * - **Local Testing**
     - Validating software in controlled development environments.

**Constraints Defined in a Deployment**:

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - **Constraint**
     - **Examples**
   * - **Processor Architectures**
     - `x86_64`, `ARM64`
   * - **Operating Systems**
     - `Linux`, `macOS`, `Windows`
   * - **Python Versions**
     - `3.8`, `3.10`

Runtime ⚙️
==========
A **Runtime** represents a specific combination of deployment parameters:

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - **Component**
     - **Description**
   * - **Architecture**
     - E.g., `ARM64`, `x86_64`
   * - **Operating System**
     - E.g., `Linux`, `macOS`
   * - **Python Runtime**
     - E.g., `CPython 3.10`, `PyPy 3.8`

This layer allows precise compatibility checks for general-purpose and specialized environments.

System 🖥️
==========
The **System** layer captures operating system details and environment configurations:

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - **Feature**
     - **Description**
   * - **Environment Variables**
     - Tracks critical variables, e.g., `DATABASE_URL`, `AUTH_TOKEN`.
   * - **Python Runtimes**
     - Identifies available Python installations for validation.

Python 🐍
=========
The **Python** layer models runtime-specific details:

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - **Detail**
     - **Description**
   * - **Implementation**
     - E.g., `CPython`, `PyPy`
   * - **Version**
     - E.g., `3.9`, `3.10`
   * - **Modules**
     - Enables runtime inspection of loaded modules for validation.

Module 📦
=========
A **Module** encapsulates metadata about Python packages or files:

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - **Metadata**
     - **Description**
   * - **Filename**
     - Location of the module on the filesystem.
   * - **Version**
     - Ensures compatibility with expected versions.
   * - **Variables**
     - Captures global variables defined within the module.
   * - **Functions**
     - Identifies available functions, their arguments, and return types.
   * - **Classes**
     - Represents classes, their attributes, methods, and inheritance hierarchies.

Class 🏛️
========
The **Class** layer focuses on Python class definitions:

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - **Feature**
     - **Description**
   * - **Attributes**
     - Tracks class-level and instance-level attributes, including types and default values.
   * - **Methods**
     - Encapsulates methods, their arguments, and return types.
   * - **Superclasses**
     - Lists the class’s inheritance hierarchy for structural consistency.

Function 🔧
===========
The **Function** layer provides detailed representations of methods and functions:

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - **Feature**
     - **Description**
   * - **Arguments**
     - Captures names, types, and default values for parameters.
   * - **Annotations**
     - Validates argument types and return types, ensuring adherence to type hints.


Unified Hierarchy for Precision 🧩
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This structured hierarchy empowers **ImportSpy** to validate an entire software stack, from deployment configurations down to individual methods within a class. This ensures alignment with developer-defined expectations at every level.

Actionable Feedback through Error Messaging 📋
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**ImportSpy** delivers clear, actionable feedback through a centralized `Errors` class. This ensures consistency and clarity when identifying issues. Examples include:

**Architecture Validation**:
- `"Invalid architecture 'arm64'. Supported architectures are: ['x86_64', 'aarch64']."`

**Environment Variables**:
- `"Missing environment variable: 'DATABASE_URL'. Ensure it is defined in the system."`
- `"Value mismatch for environment variable 'API_KEY'. Expected 'abcdef123', found 'xyz987'."`

**Class and Method Validation**:
- `"Missing class: 'UserManager'. Ensure it is defined in the module 'user_module'."`
- `"Missing method: 'save_to_db' in class 'DatabaseHandler'. Ensure it is implemented and matches the required signature."`

**Annotations**:
- `"Annotation mismatch for method 'process_data'. Expected return type 'List[str]', found 'str'."`
- `"Annotation mismatch for argument 'config' in method 'initialize'. Expected type 'dict', found 'str'."`

With this structured feedback, **ImportSpy** simplifies debugging and empowers developers to resolve issues quickly and efficiently, ensuring robust and reliable software.


These detailed and realistic diagnostic messages enable developers to identify and resolve issues effectively, reducing debugging time and increasing the robustness of integrations.

These are just a few examples of the comprehensive error feedback provided by ImportSpy. From validating environment configurations to enforcing structural and behavioral expectations, ImportSpy equips developers with a powerful toolset for ensuring consistency and reliability. 🌟

To explore all available features and error messages, **clone the repository** and start experimenting today! 🛠️ Contribute, suggest features, or report issues to help make ImportSpy even better: 🚀

.. code-block:: bash

    git clone https://github.com/atellaluca/ImportSpy

💡 Check out the documentation for detailed guides and examples on how to get started!

Sponsorship 🎉
=============

Help Build the ImportSpy Community!
--
ImportSpy is more than just a tool; it's a **movement towards smarter, safer, and more reliable Python development**. By supporting ImportSpy, you are not only helping to advance its capabilities but also contributing to the growth of an open-source project that aims to set new standards in module validation and runtime management.

Why Sponsor ImportSpy?
--
- **Accelerate Innovation**: Your contributions enable faster development of new features and quicker resolution of issues.
- **Enhance Documentation**: Support the creation of detailed guides, examples, and best practices to help the community leverage ImportSpy to its fullest.
- **Ensure Compatibility**: Help keep ImportSpy up-to-date with the latest Python versions, platforms, and architectures.
- **Foster a Thriving Community**: Sponsorship fuels outreach efforts, community events, and developer engagement.

How You Can Help
-
1. **Become a Sponsor**: Support ImportSpy on [GitHub Sponsors](https://github.com/sponsors/atellaluca).
2. **Spread the Word**: Share ImportSpy with your colleagues, communities, and networks.
3. **Contribute**: Submit pull requests, report issues, or suggest features to improve ImportSpy.

A Heartfelt Thank You 💖

Every bit of support, whether big or small, helps us take ImportSpy to the next level. Your generosity not only sustains the project but also inspires us to innovate and expand ImportSpy’s potential.

Together, let’s shape the future of Python development!

Installation ⚙️
==============

Install ImportSpy quickly and easily using pip:

.. code-block:: bash

    pip install importspy

Start integrating ImportSpy into your Python projects today and experience unparalleled control over module validation and runtime environments!

License 🔖
==========

ImportSpy is released under the MIT License, ensuring flexibility and openness for developers and contributors.

- View the full license text here: `LICENSE <https://github.com/atellaluca/ImportSpy/blob/main/LICENSE>`_

Documentation 📖
================

Dive deeper into ImportSpy's capabilities with the comprehensive documentation:

- Explore guides, examples, and API references at: `ImportSpy Docs <https://importspy.readthedocs.io>`_

Stay informed and unlock the full potential of ImportSpy in your projects!
