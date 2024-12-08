from django.shortcuts import render, redirect
from cart.cart import Cart
from store.models import Product
from django.http import JsonResponse

def wishlist(request):
    return render(request, 'wishlist.html')
