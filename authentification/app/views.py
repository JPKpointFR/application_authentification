from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from authentification import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from .token import generatorToken

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
        my_user.is_active = False
        my_user.save()
        # envoie d'email de bienvenue
        messages.success(request, "Votre compte à été créer avec succes")
        subject = "Bienvenu sur django système login"
        message = f"Salut {my_user.first_name} {my_user.last_name}\n Nous somme heureux de vous compter parmi nous\n\n\n Merci\n\n auth-systeme"
        from_email = settings.EMAIL_HOST_USER
        to_list = [my_user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=False)
        # email de confirmation
        current_site = get_current_site(request)
        email_subject = "Confirmation de l'address email sur auth-systeme"
        messageConfirm = render_to_string("emailcomfirm.html", {
            'name': my_user.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(my_user.pk)),
            'token': generatorToken.make_token(my_user),
        })

        email = EmailMessage(
            email_subject,
            messageConfirm,
            settings.EMAIL_HOST_USER,
            [my_user.email],
        )

        email.fail_sylently = False
        email.send()

        return redirect('login')
    return render(request, 'app/register.html')


def login_(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        my_user = User.objects.get(username=username)
        if user is not None:
            login(request, user)
            firstname = user.first_name
            return render(request, 'app/index.html', {'firstname': firstname})
        elif my_user.is_active == False:
            messages.error(
                request, "Vous n'avez pas confirmé votre adresse mail")
        else:
            messages.error(request, "ERREUR D'AUTHENTIFICATION")
            return redirect('login')
    return render(request, 'app/login.html')


def logout_(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecter avec succès")
    return redirect('home')


# email de confirmation
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generatorToken.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request, "Votre compte à été activé avec succes, connecter vous !!!")
        return redirect("login")
    else:
        messages.error(request, "Echec de l'activation. Veuillez réesayer !")
        return redirect("home")
