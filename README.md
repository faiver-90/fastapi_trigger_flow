# FastAPI + Kind (Kubernetes) с пробросом 8080/8443

## Запуск
```
# 0) кластер + ingress-nginx
task remove_cluster
kind create cluster --name dev --config kind-config.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
kubectl -n ingress-nginx wait --for=condition=Available --timeout=180s deploy/ingress-nginx-controller

# 1) собери ОБРАЗ тем именем, что в deployment.yaml
# если там web: app:local — собирай именно app:local
docker build -t app/auth_service:local ./app/auth_service
kind load docker-image app/auth_service:local --name dev


# 2) база и секреты
kubectl apply -f k8s/namespace.yaml
kubectl -n app apply -f k8s/postgres/postgres-secret.yaml
kubectl -n app apply -f k8s/postgres/postgres-svc.yaml
kubectl -n app apply -f k8s/postgres/postgres-statefulset.yaml

# дождись готовности БД
kubectl -n app rollout status sts/postgres
kubectl -n app get endpoints postgres

# 3) миграции (Job)
kubectl -n app apply -f k8s/postgres/alembic-migrations.yaml
kubectl -n app logs -f job/alembic-upgrade

# 4) приложение
#kubectl -n app apply -f k8s/auth_service/deployment.yaml
#kubectl -n app apply -f k8s/auth_service/service.yaml
#kubectl -n app apply -f k8s/redis.yaml
#kubectl apply -f k8s/ingress.yaml
#kubectl -n app get ingress web

kubectl apply -R -f k8s/

kubectl -n app rollout status deploy/web

# или kubectl -n app rollout status deploy

# 5) проверка цепочки ingress → service → pod
kubectl -n app get ingress web
kubectl -n app get svc web
kubectl -n app get endpoints web

# health у тебя /health_check
curl http://localhost:8080/health_check
curl http://localhost:8080/swagger
```
## Для каждого нового сервиса пишется свой deploy, service и дописывается ingress
# Быстрые диагностики
# логи web
kubectl -n app logs deploy/web

# логи job
kubectl -n app logs job/alembic-upgrade

# локальная проверка без ingress
kubectl -n app port-forward deploy/web 8001:8001
curl http://127.0.0.1:8001/health_check
