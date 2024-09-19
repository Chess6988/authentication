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

        subject = "Activate Your Account"
        message = f"Hi {user.username}, please click the following link to activate your account: {activation_link}"
        send_mail(subject, message, 'noreply@mysite.com', [user.email])
    except BadHeaderError:
        messages.error(request, "There was an error sending the activation link.")

# Signup view
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.is_active = False  # Account needs activation
                user.save()

                # Send activation email
                send_activation_email(user, request)

                # Success message
                messages.success(request, "An activation link has been sent to your email.")

                # Redirect to sign-in page after sending activation link
                return redirect('signin')
            except Exception as e:
                logger.error(f"Error creating account: {e}")
                messages.error(request, "An error occurred. Please try again.")
        else:
            if form.errors.get('email'):
                messages.error(request, "This email is already registered.")
            if form.errors.get('password2'):
                messages.error(request, "Passwords do not match.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'authentication/signup.html', {'form': form})

# Account activation view
def activate_account(request, pk):
    user = get_object_or_404(User, pk=pk)

    if not user.is_active:
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated successfully. You can now sign in.")
    else:
        messages.info(request, "Your account is already activated.")
    
    # Redirect to the sign-in page after activation
    return redirect('signin')

# Sign-in view
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, 'authentication/signin.html')

# Dashboard view
def dashboard(request):
    return render(request, 'authentication/dashboard.html')
