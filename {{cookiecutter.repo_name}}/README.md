# {{ cookiecutter.repo_name }}

## Description:
{{ cookiecutter.project_description }}


## Overview:

The project has the following packages

1. api: Provides the swagger specifications.
2. controllers: Provides the controllers that provide the method handles for operation ids specified in api.yml
3. migrations: Provides the alembic migration scripts
4. models: Provides the SQL alchemy ORM models
5. stores: Provides the persistence layer for corresponding model objects
6. tests: unit tests for various packages

Important modules

1. app.py: Provides the list of components that will be loaded during graph creation.
2. config.py: Provides default configuration overrides for the app
3. main.py: Provides the cli endpoints mainly run_server, migrate, create_all
4. wsgi.py: Used for running the app in production env using uwsgi


## Postgres

This project requires a Postgres user and a database which can be create using following SQL commands

```sql
    create database {{ cookiecutter.project_name }}_db;
    create user {{ cookiecutter.project_name }} with encrypted password 'secret';
    grant all privileges on database {{ cookiecutter.project_name }}_db to {{ cookiecutter.project_name }};
```

If there are changes to the models layer then one can generate alembic DB migration scripts using

```shell script
    migrate revision --autogenerate -m <some_message>
```

Note: You might have to fix minor things during the above step. The most common fixes are

1. Missing import statement `import microcosm_postgres`
2. If there are any UUID types then make sure that it is defined with type
`sqlalchemy_utils.types.uuid.UUIDType(binary=False)`

To run the migration scripts on the Database run

```shell script
    migrate upgrade head # instead of head, one can also provide revision
```


## Development

To setup the project for local development,

1. Create a virtualenv and install the dependencies

```shell script
    mkvirtualenv -p python3 {{ cookiecutter.project_name }}
    pip install -e .
```

2. Setup the postgres (see Postgres section, run SQL scripts and migrations scripts)

3. Start the server
```shell script
    run_server
```


## Few important notes

The service publishes several endpoints by default.

 -  The service publishes API based on the swagger spec

        GET <base path in your api.yml>

 -  The service publishes [Swagger] Spec at

        GET /<base path in your api.yml>/swagger.json

 - The service also publishes the Swagger at

        GET /<base path in your api.yml>/ui/

Note: To disable UI, please set `enable_swagger_ui` to `False` in the `config.py`


## Shoutouts

Most of this cookiecutter is gluing quite a few open source projects, some of them are

1. [microcosm]
2. [connexion]
3. [microcosm-flask]
4. [microcosm-postgres]
5. [microcosm-logging]
6. [microcosm-connexion]

[Swagger]: http://swagger.io/

[microcosm]: https://github.com/globality-corp/microcosm
[connexion]: https://github.com/zalando/connexion
[microcosm-flask]: https://github.com/globality-corp/microcosm-flask
[microcosm-postgres]: https://github.com/globality-corp/microcosm-postgres
[microcosm-logging]: https://github.com/globality-corp/microcosm-logging
[microcosm-connexion]: https://github.com/srikalyan/microcosm-connexion
