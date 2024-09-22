from django.shortcuts import render ,get_object_or_404
from django.contrib import messages



# Create your views here.
def index(request):
    return render (request, 'index.html')

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import CustomUser ,Userprofile
from django.core.mail import send_mail
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse
import os
import random

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def generate_verification_code():
    return str(random.randint(100000, 999999))

def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number  =request.POST.get('phone_number')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        date_birth =request.POST.get('date_birth')
        request.session['first_name']= first_name
        request.session['last_name']= last_name
        request.session['email']= email

        # Basic validation
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('signup')
        
        if len(password1) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect('signup')
        verification_code = generate_verification_code()
        # Create user
        user = CustomUser.objects.create_user(
            username=email,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password1,
            phone_number =phone_number,
            role='user',
            verification_code=verification_code,  # Store verification code
            is_verified=False,
            is_agreed = True,
            date_birth =date_birth  # Set is_verified to False initially
        )
        subject = "Verify Your Email"
        message = f"Hello {first_name},\n\nYour verification code is {verification_code}.\nPlease enter this code to verify your email address.\n\nThank you!"
        from_email = settings.EMAIL_HOST_USER
        to_email = [email]

        try:
            send_mail(subject, message, from_email, to_email, fail_silently=False)
            messages.success(request, "Account created! Please check your email for a verification code.")
        except Exception as e:
            messages.error(request, f"Error sending verification email: {e}")
            return redirect('signup')

        # Save profile picture if uploaded
       

 
        return redirect('verify')

    return render(request, 'signup.html')

def verify_code(request):
     if request.method == 'POST':
        code1 = request.POST.get('code1')
        code2 = request.POST.get('code2')
        code3 = request.POST.get('code3')
        code4 = request.POST.get('code4')
        code5 = request.POST.get('code5')
        code6 = request.POST.get('code6')
        first_name = request.session.get('first_name')
        last_name = request.session.get('last_name')
        email = request.session.get('email')
        entered_pin = f"{code1}{code2}{code3}{code4}{code5}{code6}"
        # Find the user with the given email and code
        try:
            user = CustomUser.objects.get(verification_code=entered_pin)
        except CustomUser.DoesNotExist:
            messages.error(request, "Invalid email or verification code.")
            return redirect('verify')

        # Mark the user as verified
        user.is_verified = True
        user.verification_code = None  # Clear the verification code
        user.save()
         # Send confirmation email
        try:
            subject = "Welcome to Experience Hotspot!"
            message = f"Hello {first_name} {last_name},\n\nThank you for signing up with Experience Hotspot. We're excited to have you onboard!\n\nFeel free to explore and book exciting experiences on our platform.\n\nBest regards,\nThe Experience Hotspot Team"
            from_email = settings.EMAIL_HOST_USER
            to_email = [email]

            send_mail(
                subject,
                message, 
                from_email,
                to_email,
                fail_silently=True,  # Set to True if you don't want it to raise errors during testing
            )
            messages.success(request, "Account created successfully! Please check your email for confirmation.")
        except Exception as e:
            messages.error(request, f"Error sending confirmation email: {e}")
            return redirect('signup')

        messages.success(request, "Your email has been verified. You can now log in.")
        return redirect('signin')

     return render (request, 'otp.html')

from django.contrib.auth import authenticate, login
from django.contrib import auth
def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate user based on email and password
        user = auth.authenticate(request, username=email, password=password)

        if user is not None:
            # Successful authentication, log in the user
            auth.login(request, user)
            messages.success(request, "You have successfully logged in!")
            return redirect('/')  # Redirect to home or dashboard after login
        else:
            # Invalid credentials
            messages.error(request, "Invalid email or password. Please try again.")
            return redirect('signin')
    return render (request, 'signin.html')

from django_countries import countries
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

def userprofile(request):
    userprofile = get_object_or_404(Userprofile, user=request.user)

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        country = request.POST.get('country')
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        zipcode = request.POST.get('zipcode')

        # Update user details
        userprofile.user.first_name = first_name
        userprofile.user.last_name = last_name
        userprofile.user.email = email
        userprofile.user.phone_number = phone_number
        userprofile.user.save()

        # Update profile details
        userprofile.country = country
        userprofile.street_address = street_address
        userprofile.city = city
        userprofile.zipcode = zipcode

        # Handle profile picture only if uploaded
        profile_picture = request.FILES.get('profile_picture')
        if profile_picture:
            userprofile.profile_picture = profile_picture

        userprofile.save()
        messages.success(request, "Profile updated successfully")
        return redirect('profile')

    context = {
        'countries': countries,  # List of countries from django-countries
        'userprofile': userprofile,
    }

    return render(request, 'profile.html', context)
def privacy(request):
    return render (request, 'privacy.html')