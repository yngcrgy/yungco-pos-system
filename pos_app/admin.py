from django.contrib import admin
from .models import Product, Transaction, TransactionItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'total', 'payment_method')
    list_filter = ('payment_method', 'date')


@admin.register(TransactionItem)
class TransactionItemAdmin(admin.ModelAdmin):
    list_display = ('transaction', 'product', 'quantity', 'subtotal')
    list_filter = ('transaction',)
