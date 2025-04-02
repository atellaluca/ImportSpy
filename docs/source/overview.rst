Overview of ImportSpy
======================

Welcome to the **ImportSpy Overview** — a complete starting point for understanding the *why*, *how*, and *where* of this project.

ImportSpy was born from a clear need:  
> How can we bring **predictability**, **security**, and **structural clarity** to Python’s dynamic import system?

This section explores not only how ImportSpy works, but also **why it exists**, the **real-world problems it solves**, and **what principles it’s built upon**. Whether you’re a developer, architect, or security engineer, this is where your journey begins.

What You’ll Find in This Section 📖
-----------------------------------

This overview is structured into three key parts, each with a distinct purpose:

The Story Behind ImportSpy
~~~~~~~~~~~~~~~~~~~~~~~~~~~

At its core, ImportSpy is more than just a tool — it’s the result of a **personal journey**.  
Created by Luca Atella as a response to burnout and routine, ImportSpy emerged from a need to **reclaim joy and meaning in development**.  
This section tells that story — not for sentiment, but to show that **structure and purpose can coexist in software**.  
*It reminds us that even small tools, built from a place of passion, can change the way we work.*

📄 :doc:`overview/story`

Use Cases in the Real World
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ImportSpy is used wherever **modular boundaries need to be enforced** — from plugin ecosystems to CI/CD pipelines.  
This section presents **detailed, practical examples** that show how ImportSpy prevents:

- Misaligned structures in dynamically loaded components
- Security flaws from unvalidated external modules
- Runtime instability across architectures or Python environments

Use cases include:

- ✅ **IoT and platform-specific integration**
- ✅ **Validation & structural integrity in plugin systems**
- ✅ **Security enforcement through runtime checks**
- ✅ **Regulatory compliance for mission-critical modules**

📄 :doc:`overview/use_cases_index`

Understanding ImportSpy’s Core
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is your **deep dive** into the internal logic and architecture of ImportSpy.

You’ll learn:

- What an **import contract** really is, and how to write one
- How the **Spy validation flow** works from import interception to enforcement
- The difference between **embedded mode** and **CLI mode**
- How runtime context (OS, Python version, architecture) plays a role
- How errors are reported and how to fix them
- Best practices for **CI/CD pipelines and integration at scale**

*This section turns concepts into confidence, and makes ImportSpy a natural extension of your development process.*

📄 :doc:`overview/understanding_importspy_index`

Let’s get started by exploring the motivation, capabilities, and inner workings of ImportSpy —  
and discover how it can help you build Python software that’s **modular, compliant, and future-ready**.

.. toctree::
   :maxdepth: 2
   :caption: 🔍 Overview

   overview/story
   overview/use_cases_index
   overview/understanding_importspy_index
