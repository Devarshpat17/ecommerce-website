# store/middleware.py
import logging
from django.http import HttpResponseForbidden
from django.shortcuts import redirect

class RequestLoggingMiddleware:
    """
    Middleware to log the details of each request for debugging purposes.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('django')

    def __call__(self, request):
        # Log request details
        self.logger.info(f"Request from IP: {request.META.get('REMOTE_ADDR')}")
        self.logger.info(f"Request Method: {request.method}")
        self.logger.info(f"Request Path: {request.path}")
        
        response = self.get_response(request)
        
        # Log response status
        self.logger.info(f"Response Status: {response.status_code}")
        return response

class AdminAccessMiddleware:
    """
    Middleware to ensure that only admin users can access certain views.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Ensure that only authenticated users can access certain views
        if view_func.__name__ in ['product_create', 'product_update', 'product_delete']:
            if not request.user.is_authenticated:
                return redirect('login')  # Redirect unauthenticated users to login page

        # Restrict access to 'product_create' view for non-admin users
        if view_func.__name__ == 'product_create' and not request.user.is_superuser:
            return HttpResponseForbidden("You do not have permission to create products.")
        
        # Optional: Restrict access to 'product_update' view for non-admin users
        if view_func.__name__ == 'product_update' and not request.user.has_perm('store.change_product'):
            return HttpResponseForbidden("You do not have permission to edit products.")
        
        # Optional: Restrict access to 'product_delete' view for non-admin users
        if view_func.__name__ == 'product_delete' and not request.user.has_perm('store.delete_product'):
            return HttpResponseForbidden("You do not have permission to delete products.")

        return None
