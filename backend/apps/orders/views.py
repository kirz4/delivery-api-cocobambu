import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from .repositories.order_repository import OrderRepository
from .domain.status_machine import InvalidTransitionError
from .services.order_service import OrderService


@csrf_exempt
@require_http_methods(["GET", "POST"])
def orders_collection(request):
    repo = OrderRepository()

    if request.method == "GET":
        return JsonResponse(repo.list(), safe=False)

    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    order_id = payload.get("order_id")
    store_id = payload.get("store_id")
    order = payload.get("order")

    if not order_id or not store_id or not isinstance(order, dict):
        return JsonResponse(
            {"error": "Fields 'order_id', 'store_id', and 'order' are required"},
            status=400,
        )

    if repo.get_by_id(order_id):
        return JsonResponse({"error": "Order already exists"}, status=409)

    created = repo.create(payload)
    return JsonResponse(created, status=201)


@csrf_exempt
@require_http_methods(["GET", "DELETE"])
def order_resource(request, order_id: str):
    repo = OrderRepository()

    if request.method == "GET":
        order = repo.get_by_id(order_id)
        if not order:
            return JsonResponse({"error": "Order not found"}, status=404)
        return JsonResponse(order, safe=False)

    ok = repo.delete(order_id)
    if not ok:
        return JsonResponse({"error": "Order not found"}, status=404)
    return JsonResponse({"deleted": True}, status=200)


@csrf_exempt
@require_http_methods(["PATCH"])
def change_order_status(request, order_id: str):
    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    new_status = payload.get("status")
    origin = payload.get("origin", "SYSTEM")

    if not new_status:
        return JsonResponse({"error": "Field 'status' is required"}, status=400)

    service = OrderService()
    try:
        updated, err = service.change_status(order_id, new_status, origin=origin)
    except InvalidTransitionError as e:
        return JsonResponse({"error": str(e)}, status=409)

    if err == "not_found":
        return JsonResponse({"error": "Order not found"}, status=404)

    if err == "invalid_storage":
        return JsonResponse({"error": "Invalid storage format"}, status=500)

    return JsonResponse(updated, safe=False, status=200)


@csrf_exempt
@require_http_methods(["GET"])
def order_allowed_statuses(request, order_id: str):
    """
    Retorna status atual + transições possíveis para o frontend renderizar botões válidos.
    """
    service = OrderService()
    data, err = service.get_allowed_next_statuses(order_id)

    if err == "not_found":
        return JsonResponse({"error": "Order not found"}, status=404)

    if err == "invalid_storage":
        return JsonResponse({"error": "Invalid storage format"}, status=500)

    return JsonResponse(data, safe=False, status=200)