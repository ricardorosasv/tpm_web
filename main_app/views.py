from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

# Create your views here.

def inicio(request):
    return render(request, 'inicio.html')

def login_page(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('inicio')

        else:
            messages.warning(request, 'Error en el nombre de usuario o contraseña.')
    
    return render(request, 'login.html',{
        'titulo' : 'Login Usuario'
    })

def logout_user(request):
    logout(request)

    return redirect('login_page')