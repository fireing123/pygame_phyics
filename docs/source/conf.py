# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


import os
import sys
sys.path.insert(0, os.path.abspath('../../'))

from recommonmark.parser import CommonMarkParser

source_parsers = {
    '.md': CommonMarkParser,
}
source_suffix = ['.rst', '.md']
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'pygame_phyics'
copyright = '2023, fireing123'
author = 'fireing123'
release = '0.3'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.doctest',
              'sphinx.ext.intersphinx', 'sphinx.ext.todo',
              'sphinx.ext.ifconfig', 'sphinx.ext.viewcode',
              'sphinx.ext.inheritance_diagram',
              'sphinx.ext.autosummary', 'recommonmark']

templates_path = ['_templates']
exclude_patterns = []

language = 'ko'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'groundwork'
html_static_path = ['_static']
