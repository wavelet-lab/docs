# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'WSDR'
copyright = 'CC BY-SA 4.0, 2025, Wavelet Lab'
author = 'Wavelet Lab'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx_copybutton',
]

# intersphinx_mapping = {
#     'python': ('https://docs.python.org/3/', None),
#     'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
# }
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'
html_logo = '_static/logo.svg'
html_theme_options = {
    "logo_only": True,
    "display_version": False,
}

# -- Options for EPUB output

epub_show_urls = 'footnote'
