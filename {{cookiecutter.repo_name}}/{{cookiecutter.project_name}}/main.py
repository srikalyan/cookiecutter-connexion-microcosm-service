"""
CLI entry points.
"""

from microcosm_postgres.createall import main as createall_main
from microcosm_postgres.migrate import main as migrate_main

from {{ cookiecutter.project_name }}.app import create_app


def create_all():
    """
    Create (and possibly drop) database tables.

    """
    graph = create_app(debug=True, model_only=True)
    createall_main(graph)


def migrate():
    """
    Invoke Alembic migrations.

    """
    graph = create_app(debug=True, model_only=True)
    migrate_main(graph)


def run_server():
    """
    Invoke Flask development server.

    """
    graph = create_app(debug=True)
    graph.connexion.run(host=graph.config.connexion.host, port=graph.config.connexion.port)


if __name__ == "__main__":
    run_server()
