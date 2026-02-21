import json
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .repositories.order_repository import OrderRepository
from .domain.status_machine import InvalidTransitionError
from .services.order_service import OrderService


@require_GET
def list_orders(request):
    repo = OrderRepository()
    return JsonResponse(repo.list(), safe=False)


@require_GET
def get_order(request, order_id: str):
    repo = OrderRepository()
    order = repo.get_by_id(order_id)
    if not order:
        return JsonResponse({"error": "Order not found"}, status=404)
    return JsonResponse(order, safe=False)

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