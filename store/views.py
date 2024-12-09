from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm
from django.contrib.auth.models import User
from django.db.models import Q


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
            messages.success(request, "Update thàn công...")
            return redirect('home')
        return render(request, 'update_user.html', {'user_form':user_form})

    return render(request, 'update_user.html', {})

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