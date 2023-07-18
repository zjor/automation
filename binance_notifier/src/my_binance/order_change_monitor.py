import json
import os
import logging
from typing import Callable

import bot_sender

from binance.client import Client

from apscheduler.schedulers.background import BlockingScheduler

from my_binance.types import BinanceOrder
from settings import get_app_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app_settings = get_app_settings()


def send_message(message):
    return bot_sender.send_message("binance", message)


def fmt_new_order(prefix: str, o: BinanceOrder):
    amount = float(o.origQty)
    price = float(o.price)
    return f"[{prefix}] {o.status} {o.type_} {o.side} {o.symbol} {amount:.4f} {price:.4f}"


def fmt_missing_order(prefix: str, old: BinanceOrder, new: BinanceOrder):
    amount = float(old.origQty)
    price = float(old.price)
    return f"[{prefix}] {old.status} -> {new.status} {old.type_} {old.side} {old.symbol} {amount:.4f} {price:.4f}"


class OrderNotifier:
    def __init__(self,
                 storage_filename: str,
                 open_orders_fetcher: Callable[[], dict[str, BinanceOrder]],
                 order_details_fetcher: Callable[[str, int], BinanceOrder],
                 prefix: str = 'SPOT'):
        self.open_orders: dict[str, BinanceOrder] = None
        self.prev_state: dict[str, BinanceOrder] = None
        self.storage_filename = storage_filename
        self.open_orders_fetcher = open_orders_fetcher
        self.order_details_fetcher = order_details_fetcher
        self.prefix = prefix

    def fetch_open_orders(self):
        logger.info("[fetch_open_orders] start")
        self.open_orders = self.open_orders_fetcher()
        logger.info(f"[fetch_open_orders] {self.open_orders}")

    def load_prev_state(self):
        if os.path.exists(self.storage_filename):
            with open(self.storage_filename, "r") as f:
                plain_dict: dict = json.load(f)
                self.prev_state = {}
                for key in plain_dict.keys():
                    self.prev_state[key] = BinanceOrder(**plain_dict[key])
            return True
        else:
            return False

    def store_open_orders(self):
        if self.open_orders is None:
            logger.info("[store_open_orders]: open_orders == None")
            return

        with open(self.storage_filename, "w") as f:
            plain_dict = {}
            for key in self.open_orders.keys():
                plain_dict[key] = self.open_orders[key].model_dump(by_alias=True)

            f.write(
                json.dumps(
                    plain_dict,
                    indent=4,
                    sort_keys=True)
            )

    def handle_order_changes(self):
        if self.open_orders is None:
            logger.info("[handle_order_changes]: open_orders == None")
            return

        if self.prev_state is None:
            logger.info("[handle_order_changes]: prev_state == None")
            return

        missing_ids: set[str] = self.prev_state.keys() - self.open_orders.keys()
        if len(missing_ids) == 0:
            logging.info("No missing orders")
        else:
            for missing_id in missing_ids:
                missing_order = self.prev_state[missing_id]
                current_order_state = self.order_details_fetcher(missing_order.symbol, missing_order.orderId)
                message = fmt_missing_order(self.prefix, missing_order, current_order_state)
                logging.info(message)
                send_message(f"`{message}`")

        new_ids: set[str] = self.open_orders.keys() - self.prev_state.keys()
        if len(new_ids) == 0:
            logging.info("No new orders")
        else:
            for new_id in new_ids:
                new_order = self.open_orders[new_id]
                message = fmt_new_order(self.prefix, new_order)
                logging.info(message)
                send_message(f"`{message}`")


def check_orders_job():
    client = Client(api_key=app_settings.BINANCE_API_KEY, api_secret=app_settings.BINANCE_SECRET)

    # Spot orders support

    def spot_order_fetcher() -> dict[str, BinanceOrder]:
        orders = client.get_open_orders()
        result = {}
        for order in orders:
            parsed = BinanceOrder(**order)
            result[parsed.clientOrderId] = parsed
        return result

    def spot_order_details_fetcher(symbol: str, order_id: int) -> BinanceOrder:
        return BinanceOrder(**client.get_order(symbol=symbol, orderId=order_id))

    logger.info("Checking spot orders")

    app = OrderNotifier(
        storage_filename='/var/tmp/binance_spot_orders.state',
        open_orders_fetcher=spot_order_fetcher,
        order_details_fetcher=spot_order_details_fetcher
    )
    app.fetch_open_orders()
    if app.load_prev_state():
        app.handle_order_changes()
    else:
        logging.warning("Previous order state does not exist")
    app.store_open_orders()

    # Margin order support

    default_symbol = 'ATOMUSDT'

    def margin_order_fetcher() -> dict[str, BinanceOrder]:
        orders = client.get_open_margin_orders(isIsolated=True, symbol=default_symbol)
        result = {}
        for order in orders:
            parsed = BinanceOrder(**order)
            result[parsed.clientOrderId] = parsed
        return result

    def margin_order_details_fetcher(symbol: str, order_id: int) -> BinanceOrder:
        return BinanceOrder(**client.get_margin_order(symbol=symbol, orderId=str(order_id), isIsolated=True))

    logger.info(f"Checking margin orders; symbol: {default_symbol}")

    margin_app = OrderNotifier(
        storage_filename='/var/tmp/binance_margin_orders.state',
        open_orders_fetcher=margin_order_fetcher,
        order_details_fetcher=margin_order_details_fetcher,
        prefix='MARGIN'
    )
    margin_app.fetch_open_orders()
    if margin_app.load_prev_state():
        margin_app.handle_order_changes()
    else:
        logging.warning("Previous order state does not exist")
    margin_app.store_open_orders()


if __name__ == "__main__":
    send_message(f"Deployed version: {os.getenv('VCS_REF')}")
    logging.info("Checking order changes on Binance")
    check_orders_job()

    scheduler = BlockingScheduler()
    scheduler.add_job(check_orders_job, "interval", minutes=1)
    scheduler.start()
