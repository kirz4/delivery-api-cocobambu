# 📦 Desafio Técnico -- Delivery App (Coco Bambu)

![CI](https://github.com/kirz4/delivery-api-cocobambu/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/kirz4/delivery-api-cocobambu/branch/main/graph/badge.svg)](https://codecov.io/gh/kirz4/delivery-api-cocobambu)

Sistema fullstack para leitura e manipulação de pedidos com:

-   🧠 Máquina de Estados para controle de status
-   💾 Persistência em arquivo JSON
-   🐳 Dockerizado
-   🧪 Testes automatizados (Backend + Frontend)
-   📊 Coverage integrado com Codecov

------------------------------------------------------------------------

# 🚀 Stack Utilizada

## Backend

-   Python 3.12
-   Django
-   Django REST Framework
-   Pytest

## Frontend

-   React
-   Vite
-   MUI (Material UI)
-   Vitest

## DevOps

-   Docker
-   Docker Compose
-   GitHub Actions (CI)
-   Codecov

------------------------------------------------------------------------

# ▶️ Como Rodar o Projeto

## ✅ Pré-requisitos

-   Docker
-   Docker Compose

## 🔥 Subindo a aplicação

Na raiz do projeto:

``` bash
docker compose up --build
```

## 🌐 Acessos

Frontend (Dashboard): http://localhost:5173

Backend (API): http://localhost:8000

Base da API: http://localhost:8000/api

------------------------------------------------------------------------

# 📂 Persistência de Dados

Os pedidos são armazenados em:

backend/data/pedidos.json

Variável utilizada:

ORDERS_JSON_PATH=/data/pedidos.json

------------------------------------------------------------------------

# 🔌 Endpoints

Base URL: http://localhost:8000/api

## 📋 Listar pedidos

``` bash
curl -i http://localhost:8000/api/orders/
```

## 🔎 Buscar pedido por ID

``` bash
curl -i http://localhost:8000/api/orders/<order_id>/
```

## ➕ Criar pedido

``` bash
curl -i -X POST http://localhost:8000/api/orders/   -H "Content-Type: application/json"   -d '{
    "store_id": "store-test-123",
    "order_id": "order-test-123",
    "order": {
      "payments": [],
      "last_status_name": "RECEIVED",
      "store": { "name": "Loja Teste", "id": "store-test-123" },
      "total_price": 15.0,
      "order_id": "order-test-123",
      "items": [],
      "created_at": 1770000000000,
      "statuses": [],
      "customer": { "name": "Cliente Teste", "temporary_phone": "+55000000000" },
      "delivery_address": {}
    }
  }'
```

## ❌ Remover pedido

``` bash
curl -i -X DELETE http://localhost:8000/api/orders/<order_id>/
```

## 🔄 Alterar status

``` bash
curl -i -X PATCH http://localhost:8000/api/orders/<order_id>/status/   -H "Content-Type: application/json"   -d '{"status":"DISPATCHED","origin":"STORE"}'
```

------------------------------------------------------------------------

# 🔁 Máquina de Estados

RECEIVED → CONFIRMED \| CANCELED\
CONFIRMED → DISPATCHED \| CANCELED\
DISPATCHED → DELIVERED \| CANCELED\
DELIVERED → Final\
CANCELED → Final

------------------------------------------------------------------------

# 🧪 Testes

## Backend

``` bash
cd backend
python -m pytest -q
```

## Frontend

``` bash
cd frontend
npm test
```

------------------------------------------------------------------------

# 📦 Estrutura do Projeto

backend/ ├── apps/ │ ├── domain/ │ ├── services/ │ ├── repositories/ │
└── views/ ├── data/ └── tests/

frontend/ ├── src/pages/ ├── components/ └── tests/

.github/workflows/ └── ci.yml

------------------------------------------------------------------------

# 👨‍💻 Autor

Lucas Cruz
