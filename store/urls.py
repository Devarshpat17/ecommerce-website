# store/urls.py
from django.urls import path
from . import views
from .views import export_admin_data
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'store'  # Needed for namespacing

urlpatterns = [
    path('', views.home, name='home'),  # Make home the default landing page
    path('products/', views.product_list, name='product_list'),
    path('create/', views.product_create, name='product_create'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/edit/', views.product_update, name='product_update'),
    path('product/<int:pk>/delete/', views.product_delete, name='product_delete'),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='auth_templates/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.signup, name='register'),  # Using existing signup view but with register URL
    
    # Password Reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='auth_templates/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='auth_templates/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='auth_templates/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='auth_templates/password_reset_complete.html'), name='password_reset_complete'),
    
    # Cart URLs
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),

    # Admin URLs
    path('custom-admin/orders/', views.admin_orders, name='admin_orders'),

    # Profile URL
    path('profile/', views.profile, name='profile'),  # Add this line
    path('profile/edit/', views.edit_profile, name='edit_profile'),  # Add this line

    # Data export URLs
    path('export-data/', views.export_data, name='export_data'),
    path('export-admin-data/', views.export_admin_data, name='export_admin_data'),
    path('api/export-admin-data/', export_admin_data, name='export_admin_data'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


