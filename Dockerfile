FROM python:3.11.4-slim-buster
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt update && apt install -y netcat libpq-dev build-essential
RUN pip install --upgrade pip
RUN pip install poetry
COPY . .
RUN poetry install

ENTRYPOINT ["/app/entrypoint.sh"]
