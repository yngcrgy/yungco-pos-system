from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-product/', views.add_product, name='add_product'),
    path('transaction/', views.process_transaction, name='process_transaction'),
    path('edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('transactions/', views.transaction_history, name='transaction_history'),
    path('transactions/<int:pk>/', views.transaction_detail, name='transaction_detail'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

]
