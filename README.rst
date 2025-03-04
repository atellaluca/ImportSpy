.. image:: https://static.pepy.tech/badge/importspy
   :target: https://pepy.tech/project/importspy

.. image:: https://img.shields.io/github/actions/workflow/status/atellaluca/ImportSpy/python-package.yml?style=flat-square
   :target: https://github.com/atellaluca/ImportSpy/actions/workflows/python-package.yml

.. image:: https://img.shields.io/github/license/atellaluca/ImportSpy?style=flat-square
   :target: https://github.com/atellaluca/ImportSpy/blob/main/LICENSE

.. image:: https://img.shields.io/readthedocs/importspy?style=flat-square
   :target: https://importspy.readthedocs.io/
   :alt: Documentation Status

ImportSpy - Intelligent Import Validation 🛡️
=============================================
**Ensure compliance, prevent unexpected failures, and enforce execution rules dynamically.**  

- 🔍 **Monitor the runtime context** before allowing imports.  
- ⚡ **Eliminate environment inconsistencies** before they break production.  
- 🛡️ **Enforce strict execution policies** for imported modules.  

.. image:: https://raw.githubusercontent.com/atellaluca/ImportSpy/refs/heads/main/assets/ImportSpy.png
   :width: 830
   :alt: ImportSpy Architecture

What is ImportSpy?
------------------

ImportSpy is a **powerful runtime validation framework** that ensures that external modules  
**only import your code in a compliant execution environment**.

Why is this important?

- ✅ **Prevents unexpected failures** caused by incorrect dependencies.  
- ✅ **Ensures security** by blocking unauthorized imports.  
- ✅ **Eliminates debugging headaches** by validating environments dynamically.  
- ✅ **Gives you full control** over how and where your code is used.

Why Should You Use ImportSpy? 🚀
--------------------------------

ImportSpy **solves real-world problems** for **Python developers, software architects, and enterprises**  
that need to **enforce execution constraints** on external modules.

🔴 **Without ImportSpy**  

- ❌ Modules may break when imported into the wrong Python version.  
- ❌ Unexpected OS configurations may introduce **silent failures**.  
- ❌ Dependencies may change, leading to **unpredictable execution issues**.  
- ❌ No **protection** against external modules misusing your code.  

🟢 **With ImportSpy**  

- ✅ **Prevent misconfigured environments from executing your code.**  
- ✅ **Block unauthorized imports and enforce runtime policies.**  
- ✅ **Ensure every imported module meets strict execution requirements.**  
- ✅ **Gain full visibility** into how your code is being used.  

How ImportSpy Works
-------------------

ImportSpy **intercepts module imports** and ensures they match **predefined execution constraints**  
before allowing execution.

The process is simple:

1. **Define execution constraints** (e.g., OS, Python version, environment variables).  
2. **ImportSpy validates runtime conditions dynamically.**  
3. **If the environment is compliant, execution proceeds.**  
4. **If the environment is non-compliant, ImportSpy blocks execution.**  

Example: Preventing Imports in the Wrong Environment
----------------------------------------------------

Imagine you want your module to be imported only in Python 3.10+, on Linux, with a specific environment variable.  
With ImportSpy, you can **enforce this automatically**.

.. code-block:: python

    from importspy.models import SpyModel, Deployment, Runtime, System, Python
    from importspy.constants import Config

    class MyModuleSpy(SpyModel):
        deployments = [
            Deployment(
                runtimes=[
                    Runtime(
                        arch=Config.ARCH_X86_64,
                        systems=[
                            System(
                                os=Config.OS_LINUX,
                                pythons=[
                                    Python(
                                        version="3.10",
                                        interpreter=Config.INTERPRETER_CPYTHON,
                                        modules=[]
                                    )
                                ],
                                envs={"CI": True}
                            )
                        ]
                    )
                ]
            )
        ]

✅ If the **importing module runs in a compliant environment**, execution proceeds.  
❌ If the **execution environment does not meet these conditions**, ImportSpy **blocks execution**.

Who Should Use ImportSpy?
-------------------------

- 🔹 **Enterprise teams** that need **strict environment control**.  
- 🔹 **Developers** working with **microservices, modular frameworks, or plugin-based architectures**.  
- 🔹 **Security-conscious projects** that want to **restrict execution contexts**.  
- 🔹 **Python package maintainers** who need **runtime validation** for external users.  

If your project **relies on external modules**, **ImportSpy is your safeguard against execution chaos**. 🔥  

Installation & Quickstart
-------------------------

ImportSpy is available on PyPI:

.. code-block:: bash

    pip install importspy

Check out the **Quickstart Guide** for step-by-step instructions.

- 📖 **Documentation**: `ImportSpy Docs <https://importspy.readthedocs.io/>`_  
- 🐍 **GitHub**: `ImportSpy Repository <https://github.com/atellaluca/ImportSpy>`_  

Support & Contribute
--------------------

ImportSpy is **open-source** and thrives with **your support**!  

Ways to Help 🚀
~~~~~~~~~~~~~~~

- ⭐ **Star the project** on GitHub → `Give it a star! <https://github.com/atellaluca/ImportSpy>`_  
- 🛠️ **Contribute** → Open issues, PRs, or improve docs.  
- 📣 **Share ImportSpy** with developers who need execution control.  
- 💖 **Sponsor ImportSpy** to support development → `Become a sponsor <https://github.com/sponsors/atellaluca>`_.  

Every contribution helps make ImportSpy **better, stronger, and more useful**!  

License
-------

ImportSpy is released under the **MIT License**.  
📜 Read the full license: `LICENSE <https://github.com/atellaluca/ImportSpy/blob/main/LICENSE>`_  

🔥 **Take control of your imports.** Start using ImportSpy today! 🚀
