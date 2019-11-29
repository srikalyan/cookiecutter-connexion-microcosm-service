from setuptools import setup, find_packages

# PLEASE DO NOT EDIT THIS, MANAGED FOR CI PURPOSES
__QUALIFIER__ = ""

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="{{ cookiecutter.project_name }}",
    version="{{ cookiecutter.project_version }}" + __QUALIFIER__,
    description="{{ cookiecutter.project_description }}",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="{{ cookiecutter.author}}",
    author_email="{{ cookiecutter.author_email }}",
    url="{{ cookiecutter.project_url }}",
    packages=find_packages(exclude=["*.tests"]),
    test_suite="{{ cookiecutter.project_name }}.tests",
    setup_requires=[
        "pytest-runner",
    ],
    install_requires=[
        "microcosm>=2,<3",
        "microcosm-connexion<=1.0.0",
        "microcosm-logging>=0.5.0",
        "microcosm-postgres>=1.17.0,<2.0.0",
        "ndg-httpsclient>=0.4.0,<1.0.0",
        "uwsgi>=2.0.13.1,<3.0.0",
    ],
    tests_require=[
        "mock",
        "pyhamcrest",
        "pytest",
        "pytest-cov",
    ],
    entry_points={
        "console_scripts": [
            "create_all = {{ cookiecutter.project_name }}.main:create_all",
            "migrate = {{ cookiecutter.project_name }}.main:migrate",
            "run_server = {{ cookiecutter.project_name }}.main:run_server",
        ],
    },
)
