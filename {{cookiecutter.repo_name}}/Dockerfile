FROM srikalyan/python_service:latest-stable

ENV APP_NAME={{ cookiecutter.project_name }}

COPY dist /tmp/dist/

RUN pip install /tmp/dist/{{ cookiecutter.project_name }}*.whl
