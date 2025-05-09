FROM python:3.11-slim AS build
ARG APP_DIR=/src

RUN apt-get update \
    && apt-get install -y \
         curl \
         build-essential \
         libffi-dev \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=1.5.1
RUN curl -sSL https://install.python-poetry.org | python - --version $POETRY_VERSION
ENV PATH /root/.local/bin:$PATH


WORKDIR ${APP_DIR}
COPY pyproject.toml poetry.lock ./
COPY . .

RUN python -m venv --copies ${APP_DIR}/venv
RUN . ${APP_DIR}/venv/bin/activate && poetry install --only main

# DEPLOYMENT RUN
FROM python:3.11-slim AS run
ARG APP_DIR=/src

COPY --from=build ${APP_DIR}/venv ${APP_DIR}/venv/
ENV PATH ${APP_DIR}/venv/bin:$PATH

WORKDIR ${APP_DIR} 
COPY . .
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

HEALTHCHECK --interval=10s --timeout=5s CMD curl --reuqest GET http://localhost:8000/health || exit 1
