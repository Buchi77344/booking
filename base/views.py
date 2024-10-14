from django.shortcuts import render ,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from math import floor




# Create your views here.

def index(request):
    # Check if the role is ' vendor'
    experiences = Experience.objects.all()
    category = Experience.CATEGORY_CHOICES

    context = {
        'experiences': experiences,
        'category':category
       
    }

    return render(request, 'index.html', context)
import re
 
@login_required(login_url='signin')
def experience(request,pk):
    experience = get_object_or_404(Experience,pk=pk)
    full_stars = int(floor(experience.rating))  # Full stars based on the rating
    half_star = experience.rating - full_stars >= 0.5  # Check if there's a half star
    empty_stars = 5 - full_stars - int(half_star)
    vendor = experience.vendor   # Remainin
    clans=experience.calendar_view
    clan =re.findall(r'[A-Za-z]{3}, [A-Za-z]{3} \d{2}',clans)
    context ={
        'experience':experience,
        'full_stars': full_stars,
        'half_star': half_star,
        'empty_stars': empty_stars,
        'vendor':vendor,
        'clan':clan
        
    }
    return render (request, 'details.html',context)

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import CustomUser ,Userprofile ,Experience
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
        return redirect('/')

     return render (request, 'otp.html')

from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.contrib import messages, auth
from django.shortcuts import render, redirect

def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate user based on email and password
        user = auth.authenticate(request, username=email, password=password)

        if user is not None:
            # Successful authentication, log in the user
            auth.login(request, user)

            # Check if the user is an admin (superuser or based on role)
            if user.is_superuser:
                # Redirect admin to the admin page
                messages.success(request, "Welcome, Admin! You have successfully logged in!")
                return redirect('admix:dashboard')  # Admin page URL
            else:
                # Redirect regular users to the home page or dashboard
                messages.success(request, "You have successfully logged in!")
                return redirect('/')
        else:
            # Invalid credentials
            messages.error(request, "Invalid email or password. Please try again.")
            return redirect('signin')

    return render(request, 'signin.html')


def logout(request):
    auth.logout(request)
    return redirect('signin')

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

import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from .models import Experience
from django.shortcuts import get_object_or_404, render
from django.conf import settings
from django.http import HttpResponse
import razorpay

def experience_payment(request, id):
    experience = get_object_or_404(Experience, id=id)
    
    # Convert the price to paisa (smallest currency unit) only for Razorpay's backend processing
    amount_in_paisa = int(experience.price * 100)  # Razorpay requires the amount in paisa

    # Ensure the amount doesn't exceed Razorpay limits
    if amount_in_paisa > 10000000:  # Max limit of ₹1,00,000
        return HttpResponse("Amount exceeds the maximum allowed limit.")

    try:
        # Initialize Razorpay client
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        # Create a Razorpay order
        order_data = {
            "amount": amount_in_paisa,  # Pass the amount in paisa
            "currency": "INR",
            "payment_capture": "1",  # Auto-capture payment after successful payment
        }
        order = client.order.create(order_data)

        # Store the order ID and experience details in session
        request.session['experience_id'] = experience.id
        request.session['order_id'] = order['id']

        # Pass the amount in rupees to the template
        context = {
            'experience': experience,
            'order_id': order['id'],
            'amount': experience.price,  # Pass the price in rupees to the template (not multiplied)
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'currency': 'INR',
        }
        return render(request, 'payment.html', context)

    except razorpay.errors.RazorpayError as e:
        return HttpResponse(f"An error occurred: {str(e)}")


from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.shortcuts import redirect
from .models import Transaction, Experience

@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        data = request.POST
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        # Extract payment details from POST data with error handling
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_signature = data.get('razorpay_signature')

        if not razorpay_order_id or not razorpay_payment_id or not razorpay_signature:
            # If any of the required fields are missing, handle the error gracefully
            return render(request, 'payment_failed.html', {
                'error': 'Payment details are missing. Please try again or contact support.'
            })

        try:
            # Verify payment signature
            client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })

            # Retrieve experience and transaction details from session
            experience_id = request.session.get('experience_id')
            if not experience_id:
                return render(request, 'payment_failed.html', {
                    'error': 'Session expired. Unable to retrieve experience details.'
                })

            experience = get_object_or_404(Experience, id=experience_id)
            amount = experience.price

            # Save the transaction details to the database
            Transaction.objects.create(
                user=request.user,
                experience=experience,
                order_id=razorpay_order_id,
                payment_id=razorpay_payment_id,
                amount=amount,
            )

            # Clear session data
            request.session.pop('experience_id', None)
            request.session.pop('order_id', None)

            # Redirect to the receipt page after successful payment
            return redirect('receipt_page')

        except razorpay.errors.SignatureVerificationError:
            # Handle payment signature verification failure
            return render(request, 'payment_failed.html', {
                'error': 'Payment verification failed. Please try again.'
            })

    return render(request, 'payment_failed.html', {
        'error': 'Invalid request method. Please use POST.'
    })



from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect

def contact (request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email =request.POST.get('email')
        message =request.POST.get('message')
                
            # Send email
        subject = f"Contact Inquiry from {name} - {settings.SITE_NAME}"
        message_body = f"You have received a new message from {name} ({email}):\n\n{message}"
        send_mail(subject, message_body, settings.EMAIL_HOST_USER, [settings.ADMIN_EMAIL])

        messages.success(request, 'your message has been sent succesfully ')
        
        return redirect('contact')  # Redirect to a success page (to be created)
   

    return render(request, 'contact.html')


def about (request):
    return render(request, 'about.html')
def faq(request):
    return render (request, 'faq.html')

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Experience, Watchlist

@login_required(login_url='signin')
def add_to_watchlist(request, experience_id):
    if request.method == 'POST':
        experience = get_object_or_404(Experience, id=experience_id)
        watchlist_item, created = Watchlist.objects.get_or_create(user=request.user, experience=experience)

        if created:
            return JsonResponse({'message': 'Experience added to watchlist'}, status=201)
        else:
            return JsonResponse({'message': 'Experience is already in your watchlist'}, status=200)
    return JsonResponse({'message': 'Invalid request method'}, status=400)
@login_required(login_url='signin')
def remove_from_watchlist(request, experience_id):
    if request.method == 'DELETE':
        experience = get_object_or_404(Experience, id=experience_id)
        watchlist_item = get_object_or_404(Watchlist, user=request.user, experience=experience)
        watchlist_item.delete()

        return JsonResponse({'message': 'Experience removed from watchlist'}, status=200)
    
@login_required(login_url='signin')
def view_watchlist(request):
    watchlist = Watchlist.objects.filter(user=request.user)
    watchlist_data = [{
        'title': item.experience.title,
        'description': item.experience.description,
        'price': item.experience.price,
        'start_date': item.experience.start_date,
        'end_date': item.experience.end_date,
        'location': item.experience.location,
        'images':item.experience.images.url,
    } for item in watchlist]

    return JsonResponse({'watchlist': watchlist_data}, status=200)

@login_required(login_url='signin')
def countwatch(request):
    count = Watchlist.objects.filter(user=request.user).count()
    return JsonResponse({'count':count},status=200)


def watch(request):
    return render (request, 'watchlist.html')

@login_required(login_url='signin')
def cart_status(request, experience_id):
    try:
        experience = Experience.objects.get(id=experience_id)
        in_cart = Watchlist.objects.filter(user=request.user, experience=experience).exists()
        return JsonResponse({'inCart': in_cart})
    except Experience.DoesNotExist:
        return JsonResponse({'error': 'Experience not found'}, status=404)

from django.db.models import Q

def search(request):
    result = []  # Initialize result
    if request.method == 'GET':
        query = request.GET.get('query', '')  # Safely retrieve query parameter

        # Filter experiences based on title, description, location, or category
        result = Experience.objects.filter(
            Q(title__icontains=query) |  # Search in the title field
            Q(description__icontains=query) |  # Search in the description field
            Q(location__icontains=query) |  # Search in the location field
            Q(category__icontains=query)  # Search in the category field
        )
        
    return render(request, 'search.html', {'result': result})
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from .models import Watchlist, Experience


import uuid
# paypal_helper.py
import paypalrestsdk
from django.conf import settings

def get_paypal_client():
    paypalrestsdk.configure({
        "mode": settings.PAYPAL_ENVIRONMENT,  # sandbox or live
        "client_id": settings.PAYPAL_CLIENT_ID,
        "client_secret": settings.PAYPAL_CLIENT_SECRET
    })


# views.py
from django.shortcuts import render, redirect, get_object_or_404
from paypalrestsdk import Payment
from .models import *


def create_paypal_order(request, experience_id):
    get_paypal_client()  # Initialize PayPal client with credentials
   
    experience = get_object_or_404(Experience, id=experience_id)
    vendor_paypal = experience.paypal
    vendor_email = vendor_paypal.paypal_email if vendor_paypal else None
    print('vendor',vendor_email)

    if not vendor_email:
        return render(request, 'payment_error.html', {"error": "Vendor does not have a PayPal email."})
    
    
    amount = experience.price

    # Create PayPal payment
    payment = Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "transactions": [{
            "amount": {
                "total": str(amount),
                "currency": "USD"
            },
            "payee": {
                "email": vendor_email  # Send payment to the vendor's PayPal account
            },
            "description": f"Payment for {experience.title}"
        }],
        "redirect_urls": {
            "return_url": request.build_absolute_uri('/payment/success/'),
            "cancel_url": request.build_absolute_uri('/payment/cancel/')
        }
    })

    if payment.create():
        # Save the transaction temporarily in the database (pending success)
        tran ,created =  Transaction.objects.get_or_create(
            user=request.user,
            experience=experience,
            order_id=payment.id,
            payment_id =uuid.uuid4,
            amount=amount,
            
        )
        tran.save()

        # Redirect the user to PayPal to approve the payment
        for link in payment.links:
            if link.rel == "approval_url":
                tran.is_paid =True
                tran.save()
                Notification.objects.create(title='Payment Successful', message=f'Payment of ${amount} for your booking "{experience.title}" has been successfully processed. Thank you!',user=request.user)
                return redirect('history')
    else:
        return render(request, 'payment_error.html', {"error": payment.error})

def payment_cancel(request):
    return render(request, 'payment_cancel.html')
 


from django.shortcuts import render, get_object_or_404
from .models import ChatMessage, Experience

from django.urls import reverse
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404, render
from .models import Experience, ChatMessage

def chat_view(request, experience_id):
    # Fetch the Experience object or return 404 if not found
    experience = get_object_or_404(Experience, id=experience_id)
    
    # Fetch messages associated with the specific experience and order by timestamp (newest first)
    messages = ChatMessage.objects.filter(experience=experience).order_by('-timestamp')

    # Generate a unique room name using username and vendor id
    room_name = f'chat_{request.user.username}_{experience.vendor.id}'

    # Render the chat template with the experience, messages, and room name
    return render(request, 'chat.html', {
        'experience': experience,
        'messages': messages,
        'room_name': room_name  # Pass the room name to the template
    })


# views.py
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

@csrf_exempt  # Consider using CSRF tokens in production
def update_status(request):
    if request.method == 'POST':
        # Check if the user is authenticated and is a vendor
      
            try:
                # Load JSON data from the request body
                data = json.loads(request.body)

                # Check the status in the request data
                status = data.get('status')
                if status == 'online':
                    # Update the vendor's status to online
                    request.user.is_online = True
                    request.user.last_activity = timezone.now()
                    request.user.save()
                    return JsonResponse({'message': 'Status updated to online'}, status=200)

                elif status == 'offline':
                    # Update the vendor's status to offline
                    request.user.is_online = False
                    request.user.save()
                    return JsonResponse({'message': 'Status updated to offline'}, status=200) 

                # If status is not recognized
                return JsonResponse({'error': 'Invalid status value'}, status=400)

            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON'}, status=400)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)

      

    # Invalid request method 
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required(login_url='signin')
def history(request):
    transaction =Transaction.objects.filter(user=request.user, is_paid =True)
    context = {
        'transaction':transaction
    }
    return render (request, 'history.html',context)

def customer(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email =request.POST.get('email')
        message =request.POST.get('message')
                
            # Send email
        subject = f"Contact Inquiry from {name} - {settings.SITE_NAME}"
        message_body = f"You have received a new message from {name} ({email}):\n\n{message}"
        send_mail(subject, message_body, settings.EMAIL_HOST_USER, [settings.ADMIN_EMAIL])

        messages.success(request, 'your message has been sent succesfully ')
        return redirect('customer')
    return render (request, 'customer.html')

@login_required(login_url='signin')
def notification(request):
    return render(request, 'notification.html')

def checkout(request):
    return render (request, 'checkout.html')


def booking(request,experience_id):
    experience = get_object_or_404(Experience, id=experience_id)
    number_of_people = 1  # Default number of guests
    price_per_guest = experience.price_per_guest  # Assuming this field exists in the Experience model

    # Calculate total price
    total_price = price_per_guest * number_of_people

    # Automatically create a booking on GET if it doesn't exist
    booking, created = Booking.objects.get_or_create(
        user=request.user,
        experience=experience,
        defaults={
            'number_of_people': number_of_people,
            'total_price': total_price
        }
    )

    if request.method == "POST":
        number_of_people = int(request.POST.get('number_of_people', 1))  # Get number of guests from form
        
        # Recalculate the total price
        total_price = price_per_guest * number_of_people
        
        # Update the booking
        booking.number_of_people = number_of_people
        booking.total_price = total_price
        booking.save()
        
        return redirect('checkout') 
    return render (request, 'checkout.html') 


def private_booking(request,experience_id):
    experience = get_object_or_404(Experience, id=experience_id)
    number_of_people = 1  # Default number of guests
    price_per_guest = experience.private_group_price 
    # Assuming this field exists in the Experience model

    # Calculate total price
    total_price = price_per_guest * number_of_people

    # Automatically create a booking on GET if it doesn't exist
    booking, created = Private_Booking.objects.get_or_create(
        user=request.user,
        experience=experience,
        defaults={
            'number_of_people': number_of_people,
            'total_price': total_price
        }
    )
    
    if request.method == "POST":
        number_of_people = int(request.POST.get('number_of_people', 1))  # Get number of guests from form
        
        # Recalculate the total price
        total_price = price_per_guest * number_of_people
        
        # Update the booking
        booking.number_of_people = number_of_people
        booking.total_price = total_price
        booking.save()
        
        return redirect('checkout') 
    return render (request, 'checkout.html') 


# Redirect to booking details page
