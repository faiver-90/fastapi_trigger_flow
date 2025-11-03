# FastAPI + Kind (Kubernetes) с пробросом 8080/8443

## Запуск
```
# 0) кластер + ingress-nginx
task remove_cluster
kind create cluster --name dev --config kind-config.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
kubectl -n ingress-nginx wait --for=condition=Available --timeout=180s deploy/ingress-nginx-controller

# 1) образы (имена ровно как в deployment.yaml)
docker build -t app/auth:local app/auth_service
kind load docker-image app/auth:local --name dev
docker build -t app/service-2:local app/service_2
kind load docker-image app/service-2:local --name dev

# 2) БД и секреты
kubectl apply -f k8s/namespace.yaml
kubectl -n app apply -f k8s/postgres/postgres-secret.yaml
kubectl -n app apply -f k8s/postgres/postgres-svc.yaml
kubectl -n app apply -f k8s/postgres/postgres-statefulset.yaml
kubectl -n app rollout status sts/postgres
kubectl -n app get endpoints postgres

# 3) миграции
kubectl -n app apply -f k8s/postgres/alembic-migrations.yaml
kubectl -n app logs -f job/alembic-upgrade

# 4) приложение, ingress, rabbit
kubectl apply -R -f k8s/

kubectl -n app rollout status deploy/auth
kubectl -n app rollout status deploy/service-2

# 5) проверки (имена ресурсов из твоего YAML)
kubectl -n app get ingress web
kubectl -n app get svc auth service-2
kubectl -n app get endpoints auth service-2
```
## Для каждого нового сервиса пишется свой deploy, service и дописывается ingress
# Быстрые диагностики
# логи web
kubectl -n app logs deploy/web

# логи job
kubectl -n app logs job/alembic-upgrade

# локальная проверка без ingress
kubectl -n app port-forward deploy/auth 8001:8001
curl http://127.0.0.1:8001/health_check

kubectl -n app port-forward deploy/service-2 8002:8002
curl http://127.0.0.1:8002/docs

# После изменения кода запускать сборку и рестарт
```
docker build -t app:local app/auth_service
kind load docker-image app:local --name dev
kubectl -n app rollout restart deploy
kubectl -n app rollout status deploy
```

# Внешний UI кролика
```
kubectl -n app port-forward deploy/rabbitmq 15672:15672
http://127.0.0.1:15672
```