"""
Configuration for the application.
"""

from microcosm.config.model import Configuration


def load_default_config(metadata):
    """
    Construct application default configuration.

    There should be very little here.

    """
    config = Configuration(
        connexion=dict(
            port=5000,
            host="0.0.0.0",
            enable_swagger_ui=True,
        ),
        logging=dict(
            levels=dict(
                override=dict(
                    warn=[],
                ),
            ),
        ),
        postgres=dict(
            password="secret",
        )
    )

    if metadata.testing:
        config.logging.levels.override.warn.append("alembic.runtime.migration")

    return config
