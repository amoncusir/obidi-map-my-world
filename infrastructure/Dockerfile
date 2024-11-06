##! NOTE
##! This Image is optimized for local development, and it's the reason about why contains 3 layers.
##! In a CI environment, should be more compacted to avoid large images and better performance on the build phase

FROM python:3.12 AS poetry

ENV PYTHONUNBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=120 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local'

RUN curl -sSL https://install.python-poetry.org | python3

FROM poetry AS env_ready

WORKDIR /opt

COPY poetry.lock pyproject.toml /opt/

RUN poetry install --only main --no-interaction --no-ansi --no-root

FROM env_ready AS final

COPY . /opt/

RUN poetry install --only main --no-interaction --no-ansi

ENTRYPOINT ["/opt/entrypoint.sh"]
