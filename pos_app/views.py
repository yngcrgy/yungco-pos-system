from django.shortcuts import render, redirect
from .models import Product, Transaction, TransactionItem
from .forms import ProductForm, TransactionItemForm
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum

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

def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductForm(instance=product)
    return render(request, 'pos_app/edit_product.html', {'form': form, 'product': product})

def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('home')
    return render(request, 'pos_app/delete_product.html', {'product': product})

def transaction_history(request):
    transactions = Transaction.objects.all().order_by('-date')
    total_sales = transactions.aggregate(Sum('total'))['total__sum'] or 0
    return render(request, 'pos_app/transaction_history.html', {
        'transactions': transactions,
        'total_sales': total_sales
    })

def transaction_detail(request, pk):
    transaction = Transaction.objects.get(pk=pk)
    items = TransactionItem.objects.filter(transaction=transaction)
    return render(request, 'pos_app/transaction_detail.html', {
        'transaction': transaction,
        'items': items
    })
