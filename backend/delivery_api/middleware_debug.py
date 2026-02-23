class DebugCorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        origin = request.META.get("HTTP_ORIGIN")
        print(">>> REQUEST ORIGIN =", origin)

        response = self.get_response(request)

        return response