# Helm chart maintenance

1. Create namespace `kubectl create namespace app-binance-notifier`
2. Create secrets:
   1. `source .env`
   2. 
```bash
kubectl create secret generic environment \
  --from-literal=TG_USER=${TG_USER} \
  --from-literal=TG_PASS=${TG_PASS} \
  --from-literal=BINANCE_API_KEY=${BINANCE_API_KEY} \
  --from-literal=BINANCE_SECRET=${BINANCE_SECRET} \
  -n app-binance-notifier
```

3. Deploy with Helm
```
helm upgrade --namespace app-binance-notifier --install binance-notifier --set version=latest ./ops/binance-notifier
```