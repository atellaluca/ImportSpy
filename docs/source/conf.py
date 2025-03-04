# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'ImportSpy'
copyright = '2024, Luca Atella'
author = 'Luca Atella'
release = '0.2.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.napoleon',
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx_tabs.tabs',
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ['_static']
html_css_files = ['custom.css']

html_theme_options = {
    "source_repository": "https://github.com/atellaluca/ImportSpy/",
    "source_branch": "main",
    "source_directory": "docs/",
}

html_theme_options["footer_icons"] = [
    {
        "name": "GitHub",
        "url": "https://github.com/atellaluca/ImportSpy",
        "html": """
            <svg stroke="currentColor" fill="currentColor" stroke-width="0"
                viewBox="0 0 24 24" height="1.5em" width="1.5em"
                xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2C6.48 2 2 6.48 2 12c0 4.42 2.87 8.17 6.84 9.49.5.09.66-.21.66-.47 0-.23-.01-.84-.01-1.64-2.78.61-3.37-1.34-3.37-1.34-.45-1.15-1.1-1.46-1.1-1.46-.9-.61.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.88 1.5 2.31 1.07 2.87.82.09-.64.35-1.07.64-1.31-2.22-.26-4.56-1.11-4.56-4.94 0-1.09.39-1.99 1.03-2.69-.1-.26-.45-1.32.1-2.75 0 0 .84-.27 2.75 1.02a9.56 9.56 0 012.5-.34c.85 0 1.7.11 2.5.34 1.91-1.29 2.75-1.02 2.75-1.02.55 1.43.2 2.49.1 2.75.64.7 1.03 1.6 1.03 2.69 0 3.84-2.34 4.67-4.58 4.92.36.31.69.93.69 1.87 0 1.35-.01 2.44-.01 2.77 0 .26.16.56.67.46C19.14 20.17 22 16.42 22 12c0-5.52-4.48-10-10-10z">
                </path>
            </svg>
        """,
        "class": "",
    },
    {
        "name": "PyPI",
        "url": "https://pypi.org/project/ImportSpy/",
        "html": """
            <svg stroke="currentColor" fill="currentColor" stroke-width="0"
                viewBox="0 0 24 24" height="1.5em" width="1.5em"
                xmlns="http://www.w3.org/2000/svg">
                <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm0 1.5c5.799 0 10.5 4.701 10.5 10.5S17.799 22.5 12 22.5 1.5 17.799 1.5 12 6.201 1.5 12 1.5zm.093 3.004c-.862.01-1.593.056-2.225.141-.632.086-1.157.207-1.603.357-.445.15-.812.34-1.125.543a3.287 3.287 0 00-.865.905c-.188.292-.292.589-.405.944-.112.355-.193.758-.249 1.293-.056.535-.087 1.124-.093 1.95L5.5 11h5V8h2v3h1.5c.759 0 1.5.647 1.5 1.5 0 .818-.682 1.5-1.5 1.5h-3c-.758 0-1.5.647-1.5 1.5v4.5h6v-3h-4v-1h3c1.79 0 3.5-1.61 3.5-3.5s-1.647-3.5-3.5-3.5h-1.5V6.5h-.407zm-2.593 8.996c.759 0 1.5.647 1.5 1.5v3h-3v-3c0-.818.682-1.5 1.5-1.5z"></path>
            </svg>
        """,
        "class": "",
    }
]
