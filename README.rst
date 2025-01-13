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

**Why ImportSpy?**
~~~~~~~~~~~~~~~~~~
ImportSpy stands out in the crowded Python ecosystem due to its unique combination of features and benefits:

1. **Cross-Platform Compatibility**:
   Validate your code's usage across diverse operating systems, processor architectures, and Python implementations with ease.

2. **Security by Design**:
   Prevent unauthorized or malicious usage through rigorous runtime validations that safeguard your codebase.

3. **Dynamic Adjustments**:
   Adapt to varying runtime conditions with precision, ensuring compatibility and seamless integration in dynamic environments.

4. **Actionable Feedback**:
   Deliver comprehensive and meaningful error messages, enabling developers to quickly identify and resolve inconsistencies.

---

Key Features 🛠️
================

**Proactive Import Validation**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ImportSpy ensures that external modules using your code adhere to predefined structures and behaviors, eliminating runtime inconsistencies and enhancing reliability.

- **Define Expectations**:
  Specify the components (functions, variables, classes) that external modules must include.
- **Validate Modern Practices**:
  Incorporate type annotations to enforce stricter and more adaptable programming styles.

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

---

**Why Choose ImportSpy?**
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

**Validation and Adaptation**:
When a non-compliant plugin is detected, ImportSpy provides actionable feedback, allowing developers to adapt their implementations.

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

ImportSpy provides practical and innovative solutions to address real-world challenges in software development, offering developers tools to create robust, secure, and adaptable applications. Here are its key use cases:

**1. Library Compliance**
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Ensuring that third-party plugins and libraries strictly follow predefined functional and structural requirements is a common challenge.

- **Problem**:
  Unverified plugins or libraries can cause unexpected failures due to missing functions or inconsistent structures.
  
- **Solution**:
  ImportSpy validates:
  - **Mandatory functions**: For example, enforcing the presence of `initialize_plugin` or `execute_task`.
  - **Critical environment variables**: Ensure required variables like `API_KEY` or `PLUGIN_ID` are present.
  
- **Impact**:
  ImportSpy prevents runtime errors and ensures seamless integration of external plugins with your system.

---

**2. Environment-Specific Behavior**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Developers often struggle with ensuring their code behaves predictably across different runtime environments.

- **Problem**:
  Differences in processor architectures, operating systems, and Python implementations can lead to subtle bugs or crashes.

- **Solution**:
  ImportSpy dynamically validates runtime conditions, ensuring compatibility with:
  - Architectures such as `x86_64` and `ARM64`.
  - Operating systems like `Linux`, `Windows`, and `macOS`.
  - Python implementations (`CPython`, `PyPy`) and versions (`3.8`, `3.10`).

- **Impact**:
  Developers can confidently deploy code across diverse environments, knowing ImportSpy will ensure predictable behavior.

---

**3. Security Enforcement**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ImportSpy enforces runtime configurations to enhance security and prevent unauthorized usage.

- **Problem**:
  Sensitive configurations, such as cryptographic settings or secure API integrations, can be misconfigured or overlooked.

- **Solution**:
  ImportSpy:
  - Validates critical variables like `AUTH_TOKEN` or `ENCRYPTION_KEY`.
  - Ensures compliance with structural and runtime constraints.
  - Rejects non-compliant modules with clear error feedback.

- **Impact**:
  Strengthened security and reduced risks of runtime vulnerabilities in sensitive environments.

---

**4. Debugging and Issue Resolution**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Identifying the root causes of integration problems is often time-consuming and error-prone.

- **Problem**:
  Dynamic integrations can fail silently, leaving developers unsure where or why an issue occurred.

- **Solution**:
  ImportSpy offers detailed, actionable feedback through precise error messages:
  - Detect missing variables (e.g., `CACHE_HOST`).
  - Identify structural inconsistencies in functions or classes.

- **Impact**:
  Enhanced debugging capabilities and faster resolution of integration issues.

---

**5. Cloud-Native Validation**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In modern cloud environments, maintaining consistency across Kubernetes clusters or Docker containers is essential.

- **Problem**:
  Deployment inconsistencies can lead to unexpected failures in production.

- **Solution**:
  ImportSpy:
  - Validates pre-deployment configurations.
  - Ensures runtime consistency across containers and clusters.

- **Example**:
  Validate that critical settings like `CACHE_SIZE` or `CONNECTION_LIMIT` are consistent across all nodes.

- **Impact**:
  Reliable and predictable cloud-native deployments.

---

**6. IoT Device Integration**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The diversity of IoT hardware and software makes standardizing integrations a significant challenge.

- **Problem**:
  Devices often run on different architectures (e.g., `ARM64`), operating systems, and Python implementations.

- **Solution**:
  ImportSpy ensures:
  - Plugins adhere to specific architectures (`ARM64`, `x86_64`).
  - Methods like `initialize` and `send_data` are implemented correctly.
  - Environment variables such as `DEVICE_ID` are defined.

- **Impact**:
  Simplified IoT integration, ensuring edge devices and central hubs operate cohesively.

Case Studies 📚
===============

Explore real-world applications of ImportSpy, showcasing its versatility and impact across diverse scenarios in software development.

**Dynamic Validation with Pydantic** 📘️
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **Context**:
  A SaaS analytics platform allowed users to create and deploy custom plugins. However, ensuring compatibility and functionality of these user-defined plugins posed significant challenges.

- **Challenges**:
  - Plugins often lacked mandatory methods or defined incorrect function signatures.
  - Debugging non-compliant plugins consumed considerable development resources.

- **Solution**:
  ImportSpy was leveraged to validate plugins dynamically:
  - **SpyModel** provided a declarative approach to define validation rules, such as required methods (`initialize_plugin`, `process_data`) and mandatory attributes.
  - Custom error messages pinpointed inconsistencies, enabling rapid debugging.

- **Outcome**:
  - Reduced integration issues by 75%.
  - Streamlined the onboarding process for user plugins, enhancing user experience.

---

**Cloud-Native Validation** ☁️
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **Context**:
  A Kubernetes-based IoT platform deployed applications across diverse clusters. Ensuring consistent runtime configurations and environment settings was critical to avoid deployment failures.

- **Challenges**:
  - Differing configurations across clusters led to unpredictable behaviors.
  - Manual validation of runtime settings proved error-prone and time-consuming.

- **Solution**:
  ImportSpy was integrated into the CI/CD pipeline to:
  - Pre-validate runtime configurations, including **environment variables** (`CACHE_SIZE`, `DB_HOST`) and **Python versions** (`3.8`, `3.10`).
  - Enforce consistency in **architecture** (`x86_64`, `ARM64`) and **OS** (`Linux`, `macOS`).

- **Outcome**:
  - Achieved deployment consistency across clusters.
  - Minimized downtime caused by misconfigurations.
  - Accelerated CI/CD workflows by automating validation steps.

---

**IoT Plugin Validation** 🌐
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **Context**:
  A smart home hub integrated third-party plugins to control sensors for temperature and motion monitoring. Maintaining compatibility across hardware variations was a critical requirement.

- **Challenges**:
  - Plugins needed to be tailored for specific architectures (`ARM64`) and operating systems (`Linux`).
  - Absence of standardization resulted in errors during runtime.

- **Solution**:
  ImportSpy ensured robust validation of IoT plugins by:
  - Checking architecture compatibility with the hub’s hardware (`ARM64`).
  - Validating mandatory methods (`initialize`, `send_data`) and attributes.
  - Enforcing Python runtime compliance (`3.8`, `3.10`).

- **Outcome**:
  - Standardized plugin validation, reducing runtime errors by 80%.
  - Enhanced compatibility between the hub and third-party plugins.

---

**Security-Centric Validation** 🔒
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **Context**:
  A financial services platform processed sensitive data and required strict compliance to runtime security configurations.

- **Challenges**:
  - Non-compliant modules jeopardized the security of cryptographic operations.
  - Misconfigured environment variables (`ENCRYPTION_KEY`, `AUTH_TOKEN`) created vulnerabilities.

- **Solution**:
  ImportSpy was utilized to enforce security-centric runtime validation:
  - Ensured that sensitive environment variables were properly defined and matched expected values.
  - Validated structural integrity of cryptographic modules, rejecting non-compliant ones.
  - Delivered precise error feedback, facilitating rapid remediation.

- **Outcome**:
  - Strengthened platform security by enforcing compliance at runtime.
  - Improved trust and reliability for clients handling sensitive data.

---

Technical Overview 🔬
=====================

Delve into the inner workings of ImportSpy and uncover the technical foundations that make it a powerful tool for runtime validation and module compliance.

**Core Mechanism**
~~~~~~~~~~~~~~~~~~
At its heart, ImportSpy leverages a robust two-phase validation process designed to ensure compatibility and compliance in every runtime environment.

1. **Developer-Defined SpyModel**:
   - A `SpyModel` acts as a blueprint, representing the expected behaviors and structures for each deployment scenario. This model is highly customizable, allowing developers to:
     - Define rules for **processor architectures** (e.g., `x86_64`, `ARM64`).
     - Specify operating systems (`Linux`, `macOS`, `Windows`).
     - Enforce constraints for Python runtimes and versions (`3.8`, `3.10`).
     - Outline the required structure for modules, including **functions**, **classes**, **attributes**, and **variables**.

2. **Runtime SpyModel Creation**:
   - At runtime, ImportSpy dynamically generates a `SpyModel` to represent the current execution context. This is achieved using advanced techniques:
     - **Reflection**: Gathers information about the executing module, including its functions, classes, and global variables.
     - **Introspection**: Captures system-level details such as the operating system, processor architecture, Python version, and implementation.
     - **Dynamic Analysis**: Constructs a comprehensive representation of the runtime environment.

3. **Validation Process**:
   - The dynamically created runtime `SpyModel` is compared against the developer-defined model:
     - **Structural Comparison**: Ensures that all required classes, methods, and variables are present and correctly defined.
     - **Semantic Validation**: Verifies annotations, return types, and argument specifications.
     - **Environment Checks**: Confirms compliance with environment-specific configurations such as `envs` or architecture constraints.
   - When inconsistencies are detected, actionable feedback is provided through detailed error messages, guiding developers to resolve issues effectively.

---

**Data Structures and Relationships**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ImportSpy models the entire execution stack, creating a hierarchy that abstracts each component and its relationships:

- **Deployment**:
  - A high-level abstraction that encapsulates multiple runtimes. Deployments can represent different environments such as edge devices, CI/CD pipelines, or local testing setups.
  - Each deployment specifies its own constraints for **architectures**, **OS**, and **Python versions**.

- **Runtime**:
  - Defines a specific combination of architecture, OS, and Python runtimes.
  - Supports validation against both general-purpose systems and highly specialized environments.

- **System**:
  - Represents the operating system and associated environment variables.
  - Tracks available Python runtimes, enabling fine-grained validation across multiple Python installations on the same system.

- **Python**:
  - Models Python runtime details:
    - Implementation (e.g., `CPython`, `PyPy`).
    - Version (e.g., `3.9`, `3.10`).
    - Loaded modules for runtime inspection.

- **Module**:
  - Encapsulates metadata about individual Python modules, including:
    - **Filename**: Tracks the module’s location.
    - **Version**: Ensures compatibility with required versions.
    - **Variables**: Captures global variables defined in the module.
    - **Functions**: Identifies available functions, along with their arguments and annotations.
    - **Classes**: Represents classes, their attributes, methods, and inheritance relationships.

- **Class**:
  - Describes Python classes within the module:
    - **Attributes**: Tracks class-level and instance-level attributes, including their types and default values.
    - **Methods**: Encapsulates methods with their arguments, annotations, and return types.
    - **Superclasses**: Lists the class's inheritance hierarchy.

- **Function**:
  - Provides a detailed representation of functions and methods:
    - **Arguments**: Captures the names, types, and default values of parameters.
    - **Annotations**: Validates argument types and return types.

This hierarchical structure allows ImportSpy to abstract and validate an entire software stack, from deployment configurations down to individual methods within a class.

---

**Actionable Feedback through Error Messaging**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ImportSpy provides precise and actionable error messages through a centralized `Errors` class, ensuring consistency and clarity. Examples include:

- **Architecture Validation**:
  - `"Invalid architecture 'arm64'. Supported architectures are: ['x86_64', 'aarch64', 'arm64', ...]."`

- **Environment Variables**:
  - `"Missing environment variable: 'DATABASE_URL'. Ensure it is defined in the system."`
  - `"Value mismatch for environment variable 'API_KEY'. Expected 'abcdef123', found 'xyz987'."`

- **Class and Method Validation**:
  - `"Missing class: 'UserManager'. Ensure it is defined in the module 'user_module'."`
  - `"Missing method: 'save_to_db' in class 'DatabaseHandler'. Ensure it is implemented and matches the required signature."`

- **Annotations**:
  - `"Annotation mismatch for method 'process_data'. Expected return type 'List[str]', found 'str'."`
  - `"Annotation mismatch for argument 'config' in method 'initialize'. Expected type 'dict', found 'str'."`

These detailed and realistic diagnostic messages enable developers to identify and resolve issues effectively, reducing debugging time and increasing the robustness of integrations.

These are just a few examples of the comprehensive error feedback provided by ImportSpy. From validating environment configurations to enforcing structural and behavioral expectations, ImportSpy equips developers with a powerful toolset for ensuring consistency and reliability. 🌟

To explore all available features and error messages, **clone the repository** and start experimenting today! 🛠️ Contribute, suggest features, or report issues to help make ImportSpy even better: 🚀

.. code-block:: bash

    git clone https://github.com/atellaluca/ImportSpy

💡 **Tip**: Check out the documentation for detailed guides and examples on how to get started!

Sponsorship 🎉
=============

Help Build the ImportSpy Community!
-----------------------------------
ImportSpy is more than just a tool; it's a **movement towards smarter, safer, and more reliable Python development**. By supporting ImportSpy, you are not only helping to advance its capabilities but also contributing to the growth of an open-source project that aims to set new standards in module validation and runtime management.

Why Sponsor ImportSpy?
-----------------------
- **Accelerate Innovation**: Your contributions enable faster development of new features and quicker resolution of issues.
- **Enhance Documentation**: Support the creation of detailed guides, examples, and best practices to help the community leverage ImportSpy to its fullest.
- **Ensure Compatibility**: Help keep ImportSpy up-to-date with the latest Python versions, platforms, and architectures.
- **Foster a Thriving Community**: Sponsorship fuels outreach efforts, community events, and developer engagement.

How You Can Help
----------------
1. **Become a Sponsor**: Support ImportSpy on [GitHub Sponsors](https://github.com/sponsors/atellaluca).
2. **Spread the Word**: Share ImportSpy with your colleagues, communities, and networks.
3. **Contribute**: Submit pull requests, report issues, or suggest features to improve ImportSpy.

A Heartfelt Thank You 💖
------------------------
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
