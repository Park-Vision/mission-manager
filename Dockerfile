FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY pyproject.toml poetry.lock ./
RUN pip3 install poetry==1.6.1
# Optimized poetry install and remove poetry cache
RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

COPY . /app/
ENV PYTHONPATH /app

EXPOSE 14550/udp
EXPOSE 9092

CMD ["poetry", "run", "python", "-m", "manager"]
