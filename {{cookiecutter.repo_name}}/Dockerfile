FROM srikalyan/python_service:latest-stable

ENV APP_NAME={{ cookiecutter.project_name }}
LABEL service-type="python-service"
LABEL uses-postgres="true"

COPY dist /tmp/dist/

RUN pip install /tmp/dist/{{ cookiecutter.project_name }}*.whl
