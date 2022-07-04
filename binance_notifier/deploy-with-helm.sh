#!/bin/bash

NS=app-binance-notifier
APP=binance-notifier
VERSION=$(git rev-parse --short HEAD)

set -x

helm upgrade --namespace ${NS} --install ${APP} --set version=${VERSION} ./ops/binance-notifier