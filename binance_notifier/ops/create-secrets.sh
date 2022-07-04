#!/bin/bash

source ../../.env

kubectl create secret generic environment \
  --from-literal=TG_USER=${TG_USER} \
  --from-literal=TG_PASS=${TG_PASS} \
  --from-literal=BINANCE_API_KEY=${BINANCE_API_KEY} \
  --from-literal=BINANCE_SECRET=${BINANCE_SECRET} \
  -n app-binance-notifier