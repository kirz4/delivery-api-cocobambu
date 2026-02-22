class DebugCorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        origin = request.META.get("HTTP_ORIGIN")
        print(">>> REQUEST ORIGIN =", origin)

        response = self.get_response(request)

        print(">>> RESPONSE ACAO =", response.headers.get("Access-Control-Allow-Origin"))
        return response