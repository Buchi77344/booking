from django.shortcuts import render
from django.contrib import messages



# Create your views here.
def index(request):
    return render (request, 'index.html')

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import CustomUser
from django.core.mail import send_mail
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse
import os


from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        profile_picture = request.FILES.get('profile_picture')

        # Basic validation
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('signup')
        
        if len(password1) < 3:
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect('signup')

        # Create user
        user = CustomUser.objects.create_user(
            username=email,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password1
        )

        # Save profile picture if uploaded
        if profile_picture:
            profile_picture_path = default_storage.save(f'profile_pictures/{user.id}_{profile_picture.name}', ContentFile(profile_picture.read()))
            user.profile_picture = profile_picture_path
            user.save()

        # Send confirmation email
        try:
            subject = "Welcome to Experience Hotspot!"
            message = f"Hello {first_name} {last_name},\n\nThank you for signing up with Experience Hotspot. We're excited to have you onboard!\n\nFeel free to explore and book exciting experiences on our platform.\n\nBest regards,\nThe Experience Hotspot Team"
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [email]

            send_mail(
                subject,
                message,
                from_email,
                to_email,
                fail_silently=False,  # Set to True if you don't want it to raise errors during testing
            )
            messages.success(request, "Account created successfully! Please check your email for confirmation.")
        except Exception as e:
            messages.error(request, f"Error sending confirmation email: {e}")
            return redirect('signup')
        # Log in the user and redirect them
        login(request, user)
        messages.success(request, "Registration successful. You are now logged in.")
        return redirect('/')

    return render(request, 'signup.html')
def signin(request):
    return render (request, 'signin.html')