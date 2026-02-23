
# 📦 Desafio Técnico — Delivery App (Coco Bambu)

![CI](https://github.com/kirz4/delivery-api-cocobambu/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/kirz4/delivery-api-cocobambu/branch/main/graph/badge.svg)](https://codecov.io/gh/kirz4/delivery-api-cocobambu)

Sistema fullstack para leitura e manipulação de pedidos com:

- 🧠 Máquina de Estados para controle de status
- 💾 Persistência em arquivo JSON
- 🐳 Dockerizado
- 🧪 Testes automatizados (Backend + Frontend)
- 📊 Coverage integrado com Codecov
- 🔁 Atualização de status com regras de negócio

---

# 🚀 Stack Utilizada

## Backend
- Python 3.12
- Django
- Django REST Framework
- Pytest
- Pytest-cov

## Frontend
- React
- Vite
- MUI (Material UI)
- Vitest

## DevOps
- Docker
- Docker Compose
- GitHub Actions (CI)
- Codecov

---

# ▶️ Como Rodar o Projeto

## ✅ Pré-requisitos
- Docker
- Docker Compose

## 🔥 Subindo a aplicação

Na raiz do projeto:

```bash
docker compose up --build
```

---

## 🌐 Acessos

Frontend (Dashboard):  
http://localhost:5173

Backend (API):  
http://localhost:8000

Base da API:  
http://localhost:8000/api

---

# 📂 Persistência de Dados

Os pedidos são armazenados em:

```
backend/data/pedidos.json
```

Variável utilizada no container:

```
ORDERS_JSON_PATH=/data/pedidos.json
```

O Docker Compose monta:

```
./backend/data → /data
```

---

# 🔌 Endpoints

Base URL:
```
http://localhost:8000/api
```

## 📋 Listar pedidos

```bash
curl -i http://localhost:8000/api/orders/
```

## 🔎 Buscar pedido por ID

```bash
curl -i http://localhost:8000/api/orders/<order_id>/
```

## ➕ Criar pedido

```bash
curl -i -X POST http://localhost:8000/api/orders/   -H "Content-Type: application/json"   -d '{ ... }'
```

## ❌ Remover pedido

```bash
curl -i -X DELETE http://localhost:8000/api/orders/<order_id>/
```

## 🔄 Alterar status

```bash
curl -i -X PATCH http://localhost:8000/api/orders/<order_id>/status/   -H "Content-Type: application/json"   -d '{"status":"DISPATCHED","origin":"STORE"}'
```

## 🔁 Consultar próximas transições

```bash
curl -i http://localhost:8000/api/orders/<order_id>/allowed-statuses/
```

---

# 🔁 Máquina de Estados

```
RECEIVED  → CONFIRMED | CANCELED
CONFIRMED → DISPATCHED | CANCELED
DISPATCHED → DELIVERED | CANCELED
DELIVERED → Final
CANCELED → Final
```

Transições inválidas retornam:

```
409 Conflict
```

---

# 🧪 Testes

## Backend

Rodar dentro do container:

```bash
docker compose exec backend pytest -q
```

Com coverage:

```bash
docker compose exec backend pytest --cov=apps --cov-report=term-missing
```

## Frontend

```bash
docker compose exec frontend npm test
```

---

# 📦 Estrutura Completa do Projeto

```
delivery-app/
│
├── backend/
│   ├── apps/
│   │   └── orders/
│   │       ├── domain/
│   │       │   └── status_machine.py
│   │       ├── repositories/
│   │       │   ├── json_storage.py
│   │       │   └── order_repository.py
│   │       ├── services/
│   │       │   └── order_service.py
│   │       ├── views.py
│   │       ├── urls_api.py
│   │       └── tests/
│   │           ├── test_api.py
│   │           ├── test_order_service.py
│   │           └── test_status_machine.py
│   │
│   ├── delivery_api/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   │
│   ├── data/
│   │   └── pedidos.json
│   │
│   ├── Dockerfile
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── OrdersDashboard.jsx
│   │   │   └── OrderDetail.jsx
│   │   ├── components/
│   │   └── lib/
│   │       └── api.js
│   │
│   ├── package.json
│   └── vite.config.js
│
├── docker-compose.yml
│
└── .github/
    └── workflows/
        └── ci.yml
```

---

# 🏗️ Arquitetura

O backend segue uma separação clara de responsabilidades:

- Domain → Regras puras (máquina de estados)
- Repository → Persistência (JSON)
- Service → Regras de negócio
- Views (DRF) → Camada HTTP
- Tests → Testes unitários e de integração

O frontend consome a API via `VITE_API_BASE_URL`, garantindo separação entre ambientes (dev/prod).

---

# 👨‍💻 Autor

Lucas Cruz
