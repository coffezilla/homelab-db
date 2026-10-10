# Homelab database service

O `docker compose` inicia um PostgreSQL e uma API Python. Os dados do banco
ficam persistidos no volume `postgres_data`.

## Executar

Defina uma senha antes de publicar o serviço no homelab:

```bash
export POSTGRES_PASSWORD='uma-senha-forte'
docker compose up -d --build
```

Endpoints:

- `POST http://<host>:8000/api/save-users`: salva um novo usuário a cada chamada.
- `POST http://<host>:8000/api/save-posts`: salva dois novos posts a cada chamada,
  associados ao usuário mais recente.
- `GET http://<host>:8000/health`: verifica se a API está disponível.

Exemplo:

```bash
curl -X POST http://<host>:8000/api/save-users
curl -X POST http://<host>:8000/api/save-posts
```

Os IDs são gerados pelo PostgreSQL e avançam progressivamente. As chamadas não
reutilizam registros existentes.

Também é possível executar os scripts diretamente no container:

```bash
docker compose exec api python save_user.py
docker compose exec api python save_posts.py
```
