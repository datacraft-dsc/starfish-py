# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import shutil
from sphinx.domains.python import PythonDomain

print(os.path.abspath('../../'))
sys.path.insert(0, os.path.abspath('../../'))

# -- Project information -----------------------------------------------------

project = 'starfish-py'
copyright = 'starfish-py contributors'
author = 'starfish-py contributors'

# The full version, including alpha/beta/rc tags
release = '0.17.4'
# The short X.Y version
release_parts = release.split('.')  # a list
version = release_parts[0] + '.' + release_parts[1] + '.' + release_parts[2]

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.intersphinx',
#    'sphinxcontrib.apidoc',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.graphviz',
    'sphinxcontrib.plantuml',
    'sphinx_automodapi.automodapi',
]

# apidoc settings
# See https://github.com/sphinx-contrib/apidoc
apidoc_module_dir = '../../starfish'
# apidoc_output_dir = 'api' by default, and leave it that way!
apidoc_separate_modules = True
# See https://www.sphinx-doc.org/en/master/man/sphinx-apidoc.html
apidoc_extra_args = []
apidoc_excluded_paths = [
  'constants.py',
  'exceptions.py',
  'logging.py',
  'middleware',
  'utils',
  'agent',
  'purchase',
  'listing',
  'account',
  'agent',
  'asset',
  'provenance.py',
  'contract',
  'network',
]

# autodoc settings
# Setting None is equivalent to giving the option name
# in the list format (i.e. it means “yes/true/on”).
# autodoc_default_options = {
#     'members': None,
#     'member-order': 'bysource',
#     'undoc-members': None,
#     'private-members': None,
#     'special-members': None,
#     'inherited-members': None,
# }

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = []

# The name of the Pygments (syntax highlig1hting) style to use.
pygments_style = 'sphinx'

highlight_language = 'python3'

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'starfishapi': ('https://datacraft-dsc.github.io/starfish-py', None)
}

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'
html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
# For the Alabaster theme, see:
# https://alabaster.readthedocs.io/en/latest/customization.html

"""
# Colors
brand_white = '#fff'
brand_black = '#141414'
brand_pink = '#ff4092'
brand_purple = '#7b1173'
brand_grey_light = '#8b98a9'
brand_grey = '#41474e'
brand_grey_dark = '#303030'

# Fonts
font_family_base = ("'Sharp Sans Medium', -apple-system, BlinkMacSystemFont, "
                    "'Segoe UI', Helvetica, Arial, sans-serif")
font_family_title = ("'Sharp Sans Display', -apple-system, "
                     "BlinkMacSystemFont, "
                     "'Segoe UI', Helvetica, Arial, sans-serif")
font_family_monospace = ("'Fira Code', 'Fira Mono', Menlo, Monaco, Consolas, "
                         "'Courier New', monospace")

html_theme_options = {
    # Colors
    'logo': 'datacraft-logo.png',
    'logo_name': True,
    'logo_text_align': 'center',
    'show_powered_by': False,
    'body_text': brand_black,
    'gray_1': brand_grey_dark,  # dark gray
    'gray_2': brand_grey_light,  # light gray
    'gray_3': brand_grey,  # medium gray
    'link': brand_pink,
    'link_hover': brand_pink,
    'pink_1': brand_pink,
    'pink_2': brand_purple,
    'sidebar_header': brand_black,
    'sidebar_link': brand_grey,
    'sidebar_list': brand_black,
    'sidebar_link_underscore': brand_white,
    'sidebar_text': brand_black,
    'code_highlight': brand_white,
    # Fonts
    'caption_font_family': font_family_base,
    'code_font_family': font_family_monospace,
    'font_family': font_family_base,
    'head_font_family': font_family_title,
}
"""

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {'sidebar.rst'}

# Delete the api/ directory of auto-generated .rst docs files
print("Removing the api/ directory via conf.py, if api/ exists.")
shutil.rmtree('api', ignore_errors=True)
print("Done removal.")

