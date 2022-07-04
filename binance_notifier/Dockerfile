FROM python:3.9

ADD requirements.txt .

RUN pip install -r requirements.txt

ADD src/*.py .

CMD ["python", "check_binance_orders.py"]