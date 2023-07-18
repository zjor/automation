FROM python:3.11

RUN pip install poetry

WORKDIR /code

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false
RUN poetry install --only main --no-root

COPY src /code

CMD ["python", "-m", "my_binance.order_change_monitor"]