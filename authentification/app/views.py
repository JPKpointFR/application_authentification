from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.


def home(request):
    return render(request, 'app/index.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        my_user = User.objects.create(username, email, password)
        my_user.firt_name = firstname
        my_user.lastt_name = lastname
        my_user.save()
        messages.success(request, "Votre compte à été créer avec succes")
        return redirect('login')
    return render(request, 'app/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            firstname = user.firstname
            return render(request, 'app/index.html', {'firstname': firstname})
        else:
            messages.error(request, "ERREUR D'AUTHENTIFICATION")
            return redirect('login')


def logout(request):
    pass
