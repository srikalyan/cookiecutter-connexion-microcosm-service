"""
Entrypoint module for WSGI containers (for production purposes)
"""

from {{ cookiecutter.project_name }}.app import create_app  # noqa


app = create_app().app
