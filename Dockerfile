FROM python:3.12-slim
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app/

COPY pyproject.toml poetry.lock ./

RUN pip install poetry 

RUN poetry install --no-interaction --no-ansi --no-root

COPY . .

CMD poetry run python -m src.main