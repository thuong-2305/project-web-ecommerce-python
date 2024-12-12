from django.contrib import admin
from .models import Category, Customer, Product, Order, Profile, Review, SaleEvent
from django.contrib.auth.models import User

admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(SaleEvent)
admin.site.register(Profile)
admin.site.register(Review)

# Mix profile info and user info
class ProfileInline(admin.StackedInline):
    model = Profile

# Extend User model
class UserAdmin(admin.ModelAdmin):
    model = User
    field = ['username', 'first_name', 'last_name', 'email']
    inlines = [ProfileInline]

# Unregister the old way
admin.site.unregister(User)

# Re-register the new way
admin.site.register(User, UserAdmin)

class ReviewAdmin(admin.ModelAdmin):
    model = Review
    fields = ['product', 'user', 'rating', 'comment', 'review_date']