from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm

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
                    
    return render(request, 'product.html', 
        {'product':product, 
         'description':description, 
         'price':price, 
         'sale_price':sale_price,
         'config':processed_config}
    )

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})

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