# Configuration file for the Sphinx documentation builder. AI Generated.

import os
import sys

sys.path.insert(0, os.path.abspath('..'))


project = 'go2-control'
copyright = '2026, 7Swaize'
author = '7Swaize'
release = '1.0.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
    'sphinx_copybutton'
]

# Mock imports for modules that may not be available
autodoc_mock_imports = [
    "pyrealsense2",
    "unitree_sdk2py",
    "iceoryx2",
    "iceoryx_interfaces",
    "fast_pointcloud"
]

# Autosummary settings
autosummary_generate = True
napoleon_numpy_docstring = True
todo_include_todos = True

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

# Use a modern, responsive theme
html_theme = 'conestack'
html_static_path = ['_static']

html_last_updated_fmt = "%Y-%m-%d"

# Optional: theme-specific options
html_theme_options = {
    "navigation_with_keys": True,
}

# -- Custom CSS tweaks -------------------------------------------------------
html_css_files = [
    'custom.css',
]

# Make copy button ignore Python REPL prompts (>>> and ...)
copybutton_prompt_text = r'>>> |\.\.\. '
copybutton_prompt_is_regexp = True


# -- Sphinx Extension API Setup ----------------------------------------------
def setup(app):
    app.add_css_file('custom.css')
