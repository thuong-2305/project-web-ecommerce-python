from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .wishlist import Wishlist
from store.models import Product
from django.http import JsonResponse

def wishlist(request):
    wishlist= Wishlist(request)
    wishlist_products = wishlist.get_prods()
    price = wishlist.get_price()
    return render(request, 'wishlist.html', {'wishlist_products':wishlist_products, 'price':price})

def wishlist_add(request):
    wishlist = Wishlist(request)
    if request.method == 'POST':
        product_id = str(request.POST.get('product_id'))
        product_price = str(request.POST.get('product_price'))

        product = get_object_or_404(Product, id=product_id)
        msg = wishlist.add(product, product_price)
        
        response = JsonResponse({'msg': msg})
        return response

def wishlist_remove(request):
    wishlist = Wishlist(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        wishlist.remove(product= product_id)

        response = JsonResponse({'product': product_id})
        messages.success(request, ("Xóa sản pẩm khỏi wishlist thành công"))
        return response
