FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends libpq5 curl \
  && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=2.2.1 PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN curl -sSL https://install.python-poetry.org | python3 - \
  && ln -s /root/.local/bin/poetry /usr/local/bin/poetry \
  && poetry config virtualenvs.create false

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root
COPY . /app

# права под нерутового
RUN chown -R 10001:0 /app && chmod -R g=u,a+rX /app
RUN chmod +x /usr/local/bin/poetry
USER 10001
EXPOSE 8002

CMD ["gunicorn","-k","uvicorn.workers.UvicornWorker","-w","2","-t","60","-b","0.0.0.0:8002","main:app"]
