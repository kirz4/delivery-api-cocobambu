# Desafio Técnico - Delivery App (Coco Bambu)

API em Django para leitura e manipulação de pedidos a partir de um
arquivo JSON (`pedidos.json`), com suporte a transição de status via
máquina de estados e persistência no próprio arquivo.

------------------------------------------------------------------------

## 🚀 Stack Utilizada

-   Python 3.12
-   Django
-   Docker + Docker Compose

------------------------------------------------------------------------

## ▶️ Como Rodar o Projeto

Na raiz do projeto:

``` bash
docker compose up --build
```

A API ficará disponível em:

    http://localhost:8000

------------------------------------------------------------------------

## 📂 Persistência de Dados

O backend lê e salva os pedidos em:

    backend/data/pedidos.json

A aplicação utiliza a variável de ambiente:

    ORDERS_JSON_PATH=/app/data/pedidos.json

------------------------------------------------------------------------

## 🔌 Endpoints

Base URL:

    http://localhost:8000/api

------------------------------------------------------------------------

### 📋 Listar pedidos

GET `/orders/`

``` bash
curl -i http://localhost:8000/api/orders/
```

------------------------------------------------------------------------

### 🔎 Buscar pedido por ID

GET `/orders/<order_id>/`

``` bash
curl -i http://localhost:8000/api/orders/<order_id>/
```

------------------------------------------------------------------------

### ➕ Criar pedido

POST `/orders/`

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

Respostas possíveis:

-   201 → Pedido criado
-   409 → Pedido já existe

------------------------------------------------------------------------

### ❌ Remover pedido

DELETE `/orders/<order_id>/`

``` bash
curl -i -X DELETE http://localhost:8000/api/orders/<order_id>/
```

Respostas possíveis:

-   200 → `{ "deleted": true }`
-   404 → Pedido não encontrado

------------------------------------------------------------------------

### 🔄 Alterar status (Máquina de Estados)

PATCH `/orders/<order_id>/status/`

Body:

``` json
{
  "status": "DISPATCHED",
  "origin": "STORE"
}
```

Exemplo:

``` bash
curl -i -X PATCH http://localhost:8000/api/orders/<order_id>/status/   -H "Content-Type: application/json"   -d '{"status":"DISPATCHED","origin":"STORE"}'
```

Respostas possíveis:

-   200 → Pedido atualizado
-   404 → Pedido não encontrado
-   409 → Transição inválida
-   400 → JSON inválido ou campo `status` ausente

------------------------------------------------------------------------

## 🔁 Máquina de Estados

Transições permitidas:

-   RECEIVED → CONFIRMED \| CANCELED
-   CONFIRMED → DISPATCHED \| CANCELED
-   DISPATCHED → DELIVERED \| CANCELED
-   DELIVERED → (final)
-   CANCELED → (final)

------------------------------------------------------------------------

## 🧪 Reset do JSON (Opcional)

Para restaurar o arquivo original de pedidos:

``` bash
cp backend/data/pedidos.seed.json backend/data/pedidos.json
docker compose restart
```

------------------------------------------------------------------------

## 📌 Observações Técnicas

-   Persistência realizada com escrita controlada em arquivo JSON.
-   PATCH isento de CSRF pois a API é consumida via cliente externo
    (curl/Insomnia).
-   Estrutura organizada em camadas:
    -   Repository
    -   Service
    -   Domain (State Machine)
    -   Views

------------------------------------------------------------------------


