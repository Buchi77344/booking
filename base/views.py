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

        # Email Subject and Recipients
        subject = 'Confirm Your Registration'
        from_email = settings.EMAIL_HOST_USER
        to_email = [email]  # Always pass a list to recipients

        # Create the plain-text and HTML message bodies
        text_content = f"Hello {first_name},\n\nThank you for registering on our platform. Please confirm your email address to start using your account."
        html_content = f"""
        <html>
        <body>
            <h1>Welcome {first_name}!</h1>
            <p>Thank you for registering on our platform. Please confirm your email address to start using your account.</p>
            <p><a href="http://example.com/confirm/{user.id}">Click here to confirm your email</a></p>
            <p>Thank you!</p>
        </body>
        </html>
        """

        # Create EmailMultiAlternatives object
        email_message = EmailMultiAlternatives(subject, text_content, from_email, to_email)

        # Attach the HTML alternative content
        email_message.attach_alternative(html_content, "text/html")

        try:
            # Send email
            email_message.send(fail_silently=False)
            messages.success(request, "A confirmation email has been sent to your email address.")
        except Exception as e:
            # Handle email sending errors
            messages.error(request, f"Error sending confirmation email: {str(e)}")
            return redirect('signup')

        # Log in the user and redirect them
        login(request, user)
        messages.success(request, "Registration successful. You are now logged in.")
        return redirect('/')

    return render(request, 'signup.html')
