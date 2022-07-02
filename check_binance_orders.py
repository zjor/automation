import json
import os
import logging

from binance.spot import Spot

import bot_sender

logging.basicConfig(level=logging.INFO)


def send_message(message):
    return bot_sender.send_message('binance', message)


def as_dict(items, get_key):
    result = {}
    for item in items:
        result[get_key(item)] = item
    return result


def fmt_new_order(o):
    status = o['status']
    _type = o['type']
    side = o['side']
    symbol = o['symbol']
    amount = float(o['origQty'])
    price = float(o['price'])
    return f"{status} {_type} {side} {symbol} {amount:.4f} {price:.4f}"


def fmt_missing_order(original, current):
    new_status = current['status']
    old_status = original['status']
    _type = original['type']
    side = original['side']
    symbol = original['symbol']
    amount = float(original['origQty'])
    price = float(original['price'])
    return f"{old_status} -> {new_status} {_type} {side} {symbol} {amount:.4f} {price:.4f}"


class OrderNotifier:
    ORDER_ID_KEY = 'clientOrderId'

    def __init__(self, api_key, secret, storage_filename='/var/tmp/binance_orders.json'):
        self.open_orders: dict[str, object] = None
        self.prev_state: dict[str, object] = None
        self.client = Spot(key=api_key, secret=secret)
        self.storage_filename = storage_filename

    def fetch_open_orders(self):
        self.open_orders = as_dict(
            self.client.get_open_orders(),
            get_key=lambda o: o[OrderNotifier.ORDER_ID_KEY])

    def load_prev_state(self):
        with open(self.storage_filename, 'r') as f:
            self.prev_state = json.load(f)

    def store_open_orders(self):
        assert self.open_orders, "open_orders == None"

        with open(self.storage_filename, 'w') as f:
            f.write(json.dumps(self.open_orders, indent=4, sort_keys=True))

    def handle_order_changes(self):
        assert self.open_orders, "open_orders == None"
        assert self.prev_state, "prev_state == None"

        missing_ids: set[str] = self.prev_state.keys() - self.open_orders.keys()
        if len(missing_ids) == 0:
            logging.info("No missing orders")
        else:
            for missing_id in missing_ids:
                missing_order = self.prev_state[missing_id]
                current_order_state = self.client.get_order(missing_order['symbol'], orderId=missing_order['orderId'])
                message = fmt_missing_order(missing_order, current_order_state)
                logging.info(message)
                send_message(f"`{message}`")

        new_ids: set[str] = self.open_orders.keys() - self.prev_state.keys()
        if len(new_ids) == 0:
            logging.info("No new orders")
        else:
            for new_id in new_ids:
                new_order = self.open_orders[new_id]
                message = fmt_new_order(new_order)
                logging.info(message)
                send_message(f"`{message}`")


if __name__ == "__main__":
    logging.info("Checking order changes on Binance")

    key, secret = os.getenv('BINANCE_API_KEY'), os.getenv('BINANCE_SECRET')

    app = OrderNotifier(key, secret)
    app.fetch_open_orders()
    app.load_prev_state()
    app.handle_order_changes()
    app.store_open_orders()
