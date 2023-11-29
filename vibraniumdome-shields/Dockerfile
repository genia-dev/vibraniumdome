FROM python:3.9 AS base

ENV POETRY_HOME=/opt/poetry
ARG POETRY_VERSION=1.5.1

RUN curl -sSL https://install.python-poetry.org | python3 - --version ${POETRY_VERSION}
RUN $POETRY_HOME/bin/poetry --version

WORKDIR /app

COPY pyproject.toml poetry.lock ./
COPY . .

RUN $POETRY_HOME/bin/poetry install --no-interaction --no-ansi

EXPOSE 5001

#ENTRYPOINT ["./docker-entrypoint.sh"]

CMD ["./docker-entrypoint.sh"]