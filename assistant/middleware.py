from django.conf import settings
from django.http import JsonResponse

class AgentAPIKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only apply this middleware to the assistant chat endpoint
        if request.path == '/assistant/chat/':
            api_key = request.headers.get('X-Agent-Key')
            if not api_key or api_key != settings.AGENT_API_KEY:
                return JsonResponse({'detail': 'Unauthorized: Invalid or missing API Key'}, status=401)
        return self.get_response(request)
