import os
import json
from pprint import pprint
from binance.spot import Spot


def as_dict(items, get_key):
    result = {}
    for item in items:
        result[get_key(item)] = item
    return result


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
            print("No missing orders")
        else:
            for missing_id in missing_ids:
                missing_order = self.prev_state[missing_id]
                current_order_state = self.client.get_order(missing_order['symbol'], orderId=missing_order['orderId'])
                print(
                    f"Order ID: {missing_order['orderId']} {missing_order['status']} -> {current_order_state['status']}")
                # TODO: status change & income if filled

        new_ids: set[str] = self.open_orders.keys() - self.prev_state.keys()
        if len(new_ids) == 0:
            print("No new orders")
        else:
            for new_id in new_ids:
                new_order = self.open_orders[new_id]
                print(f"New order ID: {new_order['orderId']}")
                pprint(new_order)
                # TODO: show expected income


if __name__ == "__main__":
    key, secret = os.getenv('BINANCE_API_KEY'), os.getenv('BINANCE_SECRET')

    app = OrderNotifier(key, secret)
    app.fetch_open_orders()
    app.load_prev_state()
    app.handle_order_changes()
    app.store_open_orders()
