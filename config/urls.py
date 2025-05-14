# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView
from django.urls import path
from store import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Other URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # Existing URL patterns
    path('login/', LoginView.as_view(), name='login'),  # Django's built-in LoginView
    path('logout/', LogoutView.as_view(), name='logout'),  # Django's built-in LogoutView
    path('signup/', views.signup, name='signup'),  # Custom signup view
    path('admin/', admin.site.urls),
    path('', include('store.urls', namespace='store')),  # Use only once, with namespace
    path('custom-admin/orders/', views.admin_orders, name='admin_orders'),

    # Include API app URLs
    


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# filepath: c:\Users\hp\myworld\ecommerce-site\store\urls.py





