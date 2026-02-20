from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .repositories.order_repository import OrderRepository

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