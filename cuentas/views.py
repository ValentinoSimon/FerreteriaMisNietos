from django.shortcuts import render
from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login , logout
from django import forms

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('lista_de_productos')
        # If form is not valid, continue to render the login form with errors
    else:
        form = AuthenticationForm()
    return render (request , 'cuentas/login.html' , { 'form' : form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('lista_de_productos')
    else:
        # For GET requests, simply redirect to the product list or login page
        return redirect('lista_de_productos')