FROM python:3.9.0-slim as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"


# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# `builder-base` stage is used to build deps + create our virtual environment
# FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        # deps for installing poetry
        curl \
        # deps for building python deps
        build-essential \
        gcc

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
ENV POETRY_VERSION=1.1.4
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

# copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH
COPY pyproject.toml ./
COPY src /src

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install --no-dev

# `development` image is used during development / testing
# FROM python-base as development

# copy in our built poetry + venv
# COPY --from=builder-base $POETRY_HOME $POETRY_HOME
# COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

# will become mountpoint of our code
# WORKDIR /app

# `production` image used for runtime
# FROM python-base as production
# ENV FASTAPI_ENV=production
# COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
# COPY ./app /app/
# WORKDIR /app
# CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app"]