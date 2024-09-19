from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm
import logging

logger = logging.getLogger(__name__)

# Function to send activation email
def send_activation_email(user, request):
    try:
        activation_link = f"https://authentication-1-3s3e.onrender.com/activate/{user.pk}/"

        subject = "Activation de votre compte"
        message = f"Bonjour {user.username}, veuillez cliquer sur ce lien pour activer votre compte : {activation_link}"
        send_mail(subject, message, 'noreply@monsite.com', [user.email])
    except BadHeaderError:
        messages.error(request, "Erreur lors de l'envoi du lien d'activation.")

# Vue d'inscription
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.is_active = False  # Le compte nécessite une activation
                user.save()

                # Envoie un email d'activation
                send_activation_email(user, request)

                # Message de succès
                messages.success(request, "Un lien sera envoyé à votre adresse email pour activer votre compte.")
                
                # Redirect to a different URL, e.g., 'signup_success'
                return redirect('signup_success')
            except Exception as e:
                logger.error(f"Erreur lors de la création du compte: {e}")
                messages.error(request, "Une erreur s'est produite. Veuillez réessayer.")
        else:
            if form.errors.get('email'):
                messages.error(request, "Cet email existe déjà.")
            if form.errors.get('password2'):
                messages.error(request, "Les mots de passe ne correspondent pas.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'authentication/signup.html', {'form': form})

# Create a success page view to show the message
def signup_success(request):
    return render(request, 'authentication/signup_success.html')

# Activation view
def activate_account(request, pk):
    user = get_object_or_404(User, pk=pk)

    if not user.is_active:
        user.is_active = True
        user.save()
        messages.success(request, "Votre compte a été activé avec succès. Vous pouvez maintenant vous connecter.")
        return redirect('signin')
    else:
        messages.info(request, "Votre compte est déjà activé.")
        return redirect('signin')

# Vue de connexion
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Ces informations n'existent pas.")
    return render(request, 'authentication/signin.html')

# Vue du tableau de bord (Dashboard view)
def dashboard(request):
    return render(request, 'authentication/dashboard.html')
