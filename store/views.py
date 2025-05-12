# store/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from .models import Product, Category, Banner, Cart, Order  # Added Cart and Order
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignupForm, ProductForm, ProfileForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('store:product_list')
    else:
        form = AuthenticationForm()
    return render(request, 'auth_templates/login.html', {'form': form})



def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store:login')  # Redirect to login page after successful signup
    else:
        form = UserCreationForm()
    return render(request, 'auth_templates/signup.html', {'form': form})



'''
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # Handle file uploads
        if form.is_valid():
            form.save()
            return redirect('store:product_list')  # Redirect to the product list or wherever you want
    else:
        form = ProductForm()

    return render(request, 'store/create_product.html', {'form': form})
'''

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('store:product_list')
    else:
        form = ProductForm()
    return render(request, 'store/product_create.html', {'form': form})



def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(name__icontains=search_query)

    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)

    # Filter by price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Sort
    sort_by = request.GET.get('sort')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'current_category': category_slug
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)  # Fetch the product based on primary key
    return render(request, 'store/product_detail.html', {'product': product})


# Update View
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.description = request.POST.get('description')
        product.save()
        return redirect('store:product_detail', pk=product.pk)
    return render(request, 'store/product_update.html', {'product': product})

# Delete View
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('store:product_list')
    return render(request, 'store/product_delete.html', {'product': product})

def home(request):
    featured_products = Product.objects.filter(is_featured=True)
    if not featured_products.exists():
        featured_products = Product.objects.all().order_by('-id')[:8]
    
    categories = Category.objects.all()
    banners = Banner.objects.all()  # Fetch banners for the carousel
    new_arrivals = Product.objects.all().order_by('-id')[:8]  # Latest 8 products

    # Ensure the user has a profile and fetch recommended products
    recommended_products = []
    if request.user.is_authenticated:
        profile, created = Profile.objects.get_or_create(user=request.user)
        recommended_products = Product.objects.filter(category__in=profile.favorite_categories.all())

    context = {
        'featured_products': featured_products,
        'categories': categories,
        'banners': banners,
        'new_arrivals': new_arrivals,
        'recommended_products': recommended_products,
    }
    return render(request, 'store/home.html', context)

@login_required
def profile(request):
    # Ensure the user has a profile
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'store/profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('store:profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'store/edit_profile.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('store:home')  # Redirect to the home page after logout

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{product.name} added to cart.")
    return redirect('store:cart')

@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.get_total_price() for item in cart_items)
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def checkout(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items:
            messages.error(request, "Your cart is empty.")
            return redirect('store:cart')

        total_price = sum(item.get_total_price() for item in cart_items)
        order = Order.objects.create(user=request.user, address=address, total_price=total_price)

        # Clear the cart
        cart_items.delete()

        messages.success(request, "Order placed successfully!")
        return redirect('store:home')

    return render(request, 'store/checkout.html')

@staff_member_required
def admin_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'store/admin_orders.html', {'orders': orders})


