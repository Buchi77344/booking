# middleware.py
from django.utils import timezone

class UpdateLastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated and is a vendor
        if request.user.is_authenticated and request.user.is_vendor:
            # Update last activity timestamp and mark as online
            request.user.last_activity = timezone.now()
            request.user.is_online = True
            request.user.save()

        response = self.get_response(request)
        return response
 