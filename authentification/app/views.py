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
        if User.objects.filter(username=username):
            messages.error(request, "Ce nom d'utilisateur est indisponible")
            return redirect('register')
        if User.objects.filter(email=email):
            messages.error(request, "Cette email est déja utilisé")
            return redirect('register')
        if not username.isalnum():
            messages.error(request, "Le username doit être alpha numérique")
            return redirect('register')
        if password != password1:
            messages.error(request, "Les mots de passe ne sont pas identiques")
            return redirect('register')

        my_user = User.objects.create_user(username, email, password)
        my_user.first_name = firstname
        my_user.last_name = lastname
        my_user.save()
        messages.success(request, "Votre compte à été créer avec succes")
        return redirect('login')
    return render(request, 'app/register.html')


def login_(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            firstname = user.first_name
            return render(request, 'app/index.html', {'firstname': firstname})
        else:
            messages.error(request, "ERREUR D'AUTHENTIFICATION")
            return redirect('login')
    return render(request, 'app/login.html')


def logout_(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecter avec succès")
    return redirect('home')
