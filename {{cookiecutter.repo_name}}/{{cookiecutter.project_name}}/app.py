"""
Create the application.

"""
import pkg_resources
from microcosm.api import create_object_graph
from microcosm.loaders import load_each, load_from_environ
from microcosm_connexion.resolver import MicrocosmResolver

from {{ cookiecutter.project_name }}.config import load_default_config
import {{ cookiecutter.project_name }}.controllers.pet  # noqa
import {{ cookiecutter.project_name }}.stores.pet  # noqa


def create_app(debug=False, testing=False, model_only=False):
    """
    Create the object graph for the application.
    """
    loader = load_each(
        load_default_config,
        load_from_environ,
    )

    graph = create_object_graph(
        name=__name__.split(".")[0],
        debug=debug,
        testing=testing,
        loader=loader,
    )

    graph.use(
        "logging",
        "postgres",
        "sessionmaker",
        "pet_store",
    )

    if not model_only:
        graph.use(
            "connexion",
            "postgres_session_factory",
            "configure_connexion_error_handler",
            "pet_controller",
        )

        api_path = pkg_resources.resource_filename(__name__, "api/api.yml")
        graph.connexion.add_api(api_path,
                                resolver=MicrocosmResolver(controller=graph.pet_controller, mark_transactional=True),
                                pythonic_params=True,
                                validate_responses=True,
                                )

    return graph.lock()
