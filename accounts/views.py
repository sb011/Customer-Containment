from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import Order, Customer, Product
from .forms import OrderForm, UserCreate, CustomerForm
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorders import unauthenticated_user, allowed_user, admin_only
from django.contrib.auth.models import Group


@unauthenticated_user
def register(request):
    form = UserCreate()
    if request.method == 'POST':
        form = UserCreate(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Accoount was created for ' + username)
            return redirect('login')
    contain = {'form': form}
    return render(request, 'accounts/register.html', contain)


@unauthenticated_user
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username and password is incorrect')
    contain = {}
    return render(request, 'accounts/login.html', contain)


def logoutpage(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
def home(request):
    customer = Customer.objects.all()
    order = Order.objects.all()
    total_order = order.count()
    delivered = order.filter(status='Delivered').count()
    pending = order.filter(status='Pending').count()
    contain = {'customer': customer, 'order': order, 'total_order': total_order,
               'delivered': delivered, 'pending': pending}
    return render(request, 'accounts/dashboard.html', contain)


@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def accountSetting(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    contain = {'form': form}
    return render(request, 'accounts/account_setting.html', contain)


@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def userpage(request):
    order = request.user.customer.order_set.all()
    total_order = order.count()
    delivered = order.filter(status='Delivered').count()
    pending = order.filter(status='Pending').count()
    contain = {'order': order, 'total_order': total_order,
               'delivered': delivered, 'pending': pending}
    return render(request, 'accounts/user.html', contain)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def product(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    order = customer.order_set.all()
    total = order.count()
    myFilter = OrderFilter(request.GET, queryset=order)
    order = myFilter.qs
    contain = {'customer': customer, 'order': order,
               'total': total, 'myFilter': myFilter}
    return render(request, 'accounts/customer.html', contain)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def createOrder(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    contain = {'form': form}
    return render(request, 'accounts/order_form.html', contain)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def updateOrder(request, pk1):
    order = Order.objects.get(id=pk1)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    contain = {'form': form}
    return render(request, 'accounts/order_form.html', contain)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def deleteOrder(request, pk2):
    order = Order.objects.get(id=pk2)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    contain = {'item': order}
    return render(request, 'accounts/delete.html', contain)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def updateCustomer(request, pk3):
    customer = Customer.objects.get(id=pk3)
    form = CustomerForm(instance=customer,)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/')
    contain = {'form': form}
    return render(request, 'accounts/update_customer.html', contain)
