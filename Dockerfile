FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN pip3 install poetry==1.6.1
# Optimized poetry install and remove poetry cache
RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

COPY . /app/
ENV PYTHONPATH /app

CMD ["poetry", "run", "python", "mission-manager"]
