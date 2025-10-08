from django.shortcuts import render, redirect
from .models import Product, Transaction, TransactionItem
from .forms import ProductForm, TransactionItemForm
from django.utils import timezone

def home(request):
    products = Product.objects.all()
    return render(request, 'pos_app/home.html', {'products': products})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductForm()
    return render(request, 'pos_app/add_product.html', {'form': form})

def process_transaction(request):
    if request.method == 'POST':
        form = TransactionItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.subtotal = item.product.price * item.quantity
            item.save()

            # create a transaction automatically
            Transaction.objects.create(
                total=item.subtotal,
                payment_method='Cash',
                date=timezone.now()
            )
            return redirect('home')
    else:
        form = TransactionItemForm()
    return render(request, 'pos_app/process_transaction.html', {'form': form})
