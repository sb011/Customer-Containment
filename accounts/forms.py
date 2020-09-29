from django.forms import ModelForm
from .models import Order, Customer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


class UserCreate(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
