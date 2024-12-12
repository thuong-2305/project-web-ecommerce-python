from django.forms import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q

from cart.cart import Cart

from payment.forms import ShippingForm
from payment.models import Order, OrderItem, ShippingAddress

from .models import Product, Category, Profile, Review, SaleEvent
from .forms import ReviewForm, SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from datetime import datetime, timedelta
import json

def review(request, pk):
    product = get_object_or_404(Product, id=pk)
    user_current = request.user
    form = ReviewForm()
    orders = Order.objects.filter(user=user_current, shipped=True)
    
    # Check if user has a recent order with the product
    has_recent_purchase = False
    orders = Order.objects.filter(user=user_current, shipped=True)
    # Lấy phần ngày, tháng, năm của ngày giao hàng và ngày hiện tại
    today = datetime.now().date()
    thirty_days_ago = today - timedelta(days=30)
    for order in orders:
        # Check if product exists in order items
        order_items = OrderItem.objects.filter(order=order, product=product)
        if order_items:  
            # Check if order is shipped within the last 30 days
            order_date = order.date_shipped.date()
            
            if order.date_shipped and order_date >= thirty_days_ago:
                has_recent_purchase = True
                break  # No need to check further orders

    if not has_recent_purchase: 
        messages.success(request, "Please buy product")
        return redirect('home')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            messages.success(request, "Đánh giá của bạn đã được gửi!")
            return redirect('home')
        else:
            messages.success(request, "Đánh giá thất bại")
            return redirect('home')
    else:
        return render(request, "review_product.html", {'form':form, 'product':product, 'pk':pk})


# def validate_review_allowed(user, product):
#     # Lấy danh sách các đơn hàng đã giao của user
    
#     for order in orders:
#         order_items = OrderItem.objects.filter(order=order, product=product)
#         if order.date_shipped and order.date_shipped >= datetime.now() - timedelta(days=30):
#             return True  # Có thể đánh giá
#     raise ValidationError("Bạn chỉ có thể đánh giá sản phẩm trong vòng 30 ngày kể từ khi giao hàng.")
    

def search(request):
    #Determine if they filled out the form
    if request.method == 'POST':
        searched = request.POST['searched']
        #Query the products from db product
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        if not searched:
            messages.success(request, "That product not exits... please again search!")
        return render(request, "search.html", {"searched" : searched})
    else:
        return render(request, "search.html", {})
    
def update_info(request):
    if request.user.is_authenticated:
        # Lấy thông tin user hiện tại
        current_user = Profile.objects.get(user__id=request.user.id)
        # Lấy thông tin vận chuyển của user hiện tại
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)

        form = UserInfoForm(request.POST or None, instance=current_user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()

            messages.success(request, "Update thành công...")
            return redirect('home')
        return render(request, 'update_info.html', {'form':form, 'shipping_form':shipping_form})
    
    else:
        messages.success(request, 'Bạn phải đăng nhập trước...')
        return redirect('home')

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        # Did they fill out the form 
        if request.method == 'POST':
            form = ChangePasswordForm(user=current_user, data=request.POST)
            # Is the form valid
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been updated...")
                login(request, current_user)
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                return redirect('update_password')
        else:
            form = ChangePasswordForm(user=current_user)
            return render(request, 'update_password.html', {'form':form})
    else:
        form = ChangePasswordForm(request, "Please log in to update your password.")
        return redirect('home')
    
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
    
        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "Update thành công...")
            return redirect('home')
        return render(request, 'update_user.html', {'user_form':user_form})

    else:
        messages.success(request, 'Bạn phải đăng nhập trước...')
        return redirect('home')

def category_summary(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'category_summary.html', {'categories':categories, 'products':products})

def category(request, foo):
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category})
    except:
        messages.success("That category don' exits...")
        return redirect('home')

def product(request, pk):
    product = Product.objects.get(id=pk)
    price = f"{product.price:,}"
    sale_price = f"{product.sale_price:,}"
    description = product.description.split("    ")
    config = product.config.split("- ")
    processed_config =[
        {parts[0]: [{kv.split(": ")[0]: kv.split(": ")[1]} for kv in parts[1:] if ": " in kv]}
        for con in config if con
        for parts in [con.split(" + ")]]
    
    reviews = Review.objects.filter(product=product)  

    return render(request, 'product.html', 
        {'product':product, 
         'description':description, 
         'price':price, 
         'sale_price':sale_price,
         'config':processed_config,
         'reviews' : reviews}
    )

def home(request):
    products = Product.objects.all()

    # Lấy các sự kiện giảm giá còn hiệu lực
    active_sales = SaleEvent.objects.filter(
        start_date__lte=datetime.now(),
        end_date__gte=datetime.now()
    )
    # Lấy danh sách các category được giảm giá
    discounted_categories = [sale.category for sale in active_sales]
    context = {
        'products':products,
        'discounted_categories': discounted_categories,
    }

    return render(request, 'home.html', context)

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        error = ''
        if user is not None:
            login(request, user)

            # Do some shopping cart stuff
            current_user = Profile.objects.get(user__id=request.user.id)
            # Get their saved cart from database
            save_cart = current_user.old_cart
            if save_cart:
                # Convert dictionary using JSON
                converted_cart = json.loads(save_cart)
                # Add the loaded cart dictionary to our session
                # Get the cart
                cart = Cart(request)
                # Loop through the cart and add the items from the database
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)

            messages.success(request, ('Bạn đã đăng nhập thành công.'))
            return redirect('home')
        else:
            error = 'Tài khoản không đúng.'
            return render(request, 'login.html', {'error':error})
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ('Bạn đã đăng xuất tài khoản hiện tài!'))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have register successfull! Welcome"))
            return redirect('home')
        else:
            errors = form.errors
            return render(request, 'register.html', {'form':form, 'errors':errors})
    else:        
        return render(request, 'register.html', {'form':form})

# Cho vao ham home 
# def show_discount(request):
#     # Lấy các sự kiện giảm giá còn hiệu lực
#     active_sales = SaleEvent.objects.filter(
#         start_date__lte=datetime.now(),
#         end_date__gte=datetime.now()
#     )
#     # Lấy danh sách các category được giảm giá
#     discounted_categories = [sale.category for sale in active_sales]
#     context = {
#         'discounted_categories': discounted_categories,
#     }
#     return render(request, 'home.html', context)