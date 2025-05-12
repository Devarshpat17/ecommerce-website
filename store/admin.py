from django.contrib import admin
from .models import Product, Category, Banner, Cart, Order  # Import Order model

admin.site.register(Product)

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    list_filter = ('is_active',)

# Register the Order model
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'address', 'total_price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'address')