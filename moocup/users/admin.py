from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Product


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'date_joined', 'product_code']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'timestamp']
