FROM python:3.10

EXPOSE 50051

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1

RUN pip install poetry

WORKDIR /opt/app
COPY COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

COPY src .

RUN ["chmod", "+x", "/opt/app/entrypoint.sh"]
CMD ["/opt/app/entrypoint.sh"]