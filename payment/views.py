from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from cart.cart import Cart
from payment.forms import PaymentForm, ShippingForm
from payment.models import Order, ShippingAddress, OrderItem
from store.models import Profile

def orders(request, pk):
    if request.user.is_authenticated:
        order = Order.objects.get(id=pk)
        items = OrderItem.objects.filter(order=pk)
        return render(request, 'payment/orders.html', {'order':order, 'items':items})
    else:
        messages.success(request, "Access Dinied")
        return redirect('home')

def not_shipped_dash(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(shipped=False, user=request.user).order_by('-date_ordered', '-id')
        return render(request, 'payment/not_shipped_dash.html', {'orders':orders})
    else:
        messages.success(request, "Access Dinied")
        return redirect('home')

def shipped_dash(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(shipped=True, user=request.user).order_by('-date_ordered', '-id')
        return render(request, 'payment/shipped_dash.html', {'orders': orders})
    else:
        messages.success(request, "Access Dinied")
        return redirect('home')

def payment_success(request):
    return render(request, 'payment/payment_success.html', {})

def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods 
    quantities = cart.get_quants
    totals = cart.total()
    total_final = cart.total_final()

    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, 'payment/checkout.html', {'cart_products':cart_products, 'quantities': quantities, 'totals':totals, 'shipping_form':shipping_form, 'total_final':total_final})
    else:
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'payment/checkout.html', {'cart_products':cart_products, 'quantities': quantities, 'totals':totals, 'shipping_form':shipping_form, 'total_final':total_final})


def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods 
        quantities = cart.get_quants
        totals = cart.total()
        shipping_method = cart.shipping_method
        price_ship = cart.get_shipping_cost(shipping_method)
        total_final = cart.total_final()

        #  Create a session with Shipping info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        # Chech see if user logged in 
        if request.user.is_authenticated:
            # Get billing form 
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {'cart_products':cart_products, 'quantities': quantities, 'totals':totals, 'total_final':total_final, 'shipping_method':shipping_method, 'price_ship':price_ship, 'shipping_info':request.POST, 'billing_form':billing_form})
        else:
            billing_form = PaymentForm()
            shipping_form = ShippingForm(request.POST or None)
            return render(request, 'payment/billing_info.html', {'cart_products':cart_products, 'quantities': quantities, 'totals':totals, 'total_final':total_final, 'shipping_method':shipping_method, 'price_ship':price_ship, 'shipping_form':shipping_form, 'billing_form':billing_form})
    else:
        messages.success(request, "Access Cancled")
        return redirect('home')
    
def process_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods 
        quantities = cart.get_quants
        totals = cart.total_final()

        # Get billing info from card 
        payment_form = PaymentForm(request.POST or None)

        # Get shipping Session data
        my_shipping = request.session.get('my_shipping')

        # Create Shipping info from session info
        full_name = my_shipping['shipping_full_name']
        phone = my_shipping['shipping_phone']
        shipping_address = f"{my_shipping['shipping_address']}\n{my_shipping['shipping_state']}"
        amount_paid = totals

        if request.user.is_authenticated:
            #logged in
            user = request.user
            # create Order 
            create_order = Order(user=user, full_name=full_name, phone=phone, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            # Add order item
            # Get order id
            order_id = create_order.pk
            # Get product id
            for product in cart_products():
                product_id = product.id
                
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                for key, value in quantities().items():
                    if int(key) == product.id:
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
                        create_order_item.save()

            # Delete out of products cart when buyed
            for key in list(request.session.keys()):
                if key == 'session_key':
                    del request.session[key]

            # Delete our cart from db when buyed success
            current_user = Profile.objects.filter(user__id=request.user.id)
            current_user.update(old_cart='')

            messages.success(request, "Payment successful!")
            return redirect('home')
        else:
            messages.success(request, "Please login or register to buy products...")
            return redirect('home')
    else:
        messages.success(request, "Access Cancled")
        return redirect('home')
    

def process_order_paypal(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods 
        quantities = cart.get_quants
        totals = cart.total_final()

        # Get billing info from card 
        payment_form = PaymentForm(request.POST or None)

        # Get shipping Session data
        my_shipping = request.session.get('my_shipping')

        # Create Shipping info from session info
        full_name = my_shipping['shipping_full_name']
        phone = my_shipping['shipping_phone']
        shipping_address = f"{my_shipping['shipping_address']}\n{my_shipping['shipping_state']}"
        amount_paid = totals

        if request.user.is_authenticated:
            #logged in
            user = request.user
            # create Order 
            create_order = Order(user=user, full_name=full_name, phone=phone, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            # Add order item
            # Get order id
            order_id = create_order.pk
            # Get product id
            for product in cart_products():
                product_id = product.id
                
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                for key, value in quantities().items():
                    if int(key) == product.id:
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
                        create_order_item.save()

            # Delete out of products cart when buyed
            for key in list(request.session.keys()):
                if key == 'session_key':
                    del request.session[key]

            # Delete our cart from db when buyed success
            current_user = Profile.objects.filter(user__id=request.user.id)
            current_user.update(old_cart='')

            messages.success(request, "Payment successful!")
            return redirect('home')
        else:
            messages.success(request, "Please login or register to buy products...")
            return redirect('home')
    

    
def process_order_upon(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods 
        quantities = cart.get_quants
        totals = cart.total_final()

        # Get billing info from card 
        payment_form = PaymentForm(request.POST or None)

        # Get shipping Session data
        my_shipping = request.session.get('my_shipping')

        # Create Shipping info from session info
        full_name = my_shipping['shipping_full_name']
        phone = my_shipping['shipping_phone']
        shipping_address = f"{my_shipping['shipping_address']}\n{my_shipping['shipping_state']}"
        amount_paid = totals

        if request.user.is_authenticated:
            #logged in
            user = request.user
            # create Order 
            create_order = Order(user=user, full_name=full_name, phone=phone, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            # Add order item
            # Get order id
            order_id = create_order.pk
            # Get product id
            for product in cart_products():
                product_id = product.id
                
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                for key, value in quantities().items():
                    if int(key) == product.id:
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
                        create_order_item.save()

            # Delete out of products cart when buyed
            for key in list(request.session.keys()):
                if key == 'session_key':
                    del request.session[key]

            # Delete our cart from db when buyed success
            current_user = Profile.objects.filter(user__id=request.user.id)
            current_user.update(old_cart='')

            messages.success(request, "Payment successful!")
            return redirect('home')
        else:
            messages.success(request, "Please login or register to buy products...")
            return redirect('home')
