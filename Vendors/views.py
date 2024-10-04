from django.shortcuts import render ,get_object_or_404

# Create your views here.


from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.core.mail import send_mail
from base.models import CustomUser ,Experience,VendorProfile
from django.conf import settings

from django.shortcuts import render, redirect
from django.contrib import messages
from base.models import CustomUser
from django.contrib.auth import login

def signup(request):
    if request.method == 'POST':
        # Retrieve form data from POST request
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
       
        # Check for password match
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')  # Return to signup page if error

        # Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('signup')  # Return to signup page if email exists
        
        # Store data temporarily in session (in case of multi-step registration)
        request.session['first_name'] = first_name
        request.session['last_name'] = last_name
        request.session['email'] = email
        request.session['password'] = password
     
        # Redirect to vendor signup to complete additional details
        return redirect('signup_vendor')
    
    return render(request, 'vendor/signup.html')


def signup_vendor(request):
    # Retrieve the session data for the first step
    first_name = request.session.get('first_name')
    last_name = request.session.get('last_name')
    email = request.session.get('email')
    password = request.session.get('password')

    # Ensure that the first step data is available
    if not first_name or not last_name or not email or not password:
        messages.error(request, "Please complete the first step of registration.")
        return redirect('signup')  # If session data is not found, redirect to signup
    
    if request.method == "POST":
        # Retrieve additional data from POST request
        phone_number = request.POST.get('phone_number')
        business_name = request.POST.get('business_name')
        vendor_type = request.POST.get('vendor_type')

        # Create new vendor user with the gathered data
        try:
            vendor = CustomUser.objects.create_user(
                username=email,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                phone_number=phone_number,
                business_name=business_name,
                vendor_type=vendor_type,
                role='vendor',  # Setting role as vendor
            )

            # Log in the user after successful registration
           

            # Clear session data after use
            request.session.flush()

            messages.success(request, "Vendor registered successfully!")
            return redirect('home')  # Redirect to home or vendor dashboard after signup
        
        except Exception as e:
            messages.error(request, f"Error creating vendor: {str(e)}")
            return redirect('signup_vendor')
    
    return render(request, 'vendor/signup_vendor.html')



from django.contrib.auth import authenticate, login
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate user based on email and password
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Successful authentication, log in the user
            login(request, user)
            messages.success(request, "You have successfully logged in!")
            return redirect('home')  # Redirect to home or dashboard after login
        else:
            # Invalid credentials
            messages.error(request, "Invalid email or password. Please try again.")
            return redirect('login')

    return render(request, 'vendor/login.html')



# views.py

from django.shortcuts import render, redirect
from base.models import Experience
from django.core.files.storage import FileSystemStorage  # For handling image upload

def create_experience(request):
    if request.method == 'POST':
        # Retrieve form data
        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('category')
        location = request.POST.get('location')
        price = request.POST.get('price')
        available_slots = request.POST.get('available_slots')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        tags = request.POST.get('tags')
        duration = request.POST.get('duration')
        requirements = request.POST.get('requirements')
        what_to_bring = request.POST.get('what_to_bring')
        images = request.FILES.get('images')
        # Assuming the user has a VendorProfile
        vendor_profile =get_object_or_404 (VendorProfile, user=request.user)
        if not Vendorpaypal.objects.filter(user=request.user).exists():
            return redirect('vendor:payment')
        vendor = get_object_or_404(Vendorpaypal,user=request.user)
        vendor_paypal = vendor.paypal_email
        

        # Create the Experience instance
        new_experience = Experience.objects.create(
            title=title,
            description=description,
            category=category,
            location=location,
            price=price,
            available_slots=available_slots,
            start_date=start_date,
            end_date=end_date,
            vendor=vendor_profile,
            paypal =vendor_paypal,
            tags=tags,
            duration=duration,
            requirements=requirements,
            what_to_bring=what_to_bring,
            images=images
        )

        # Redirect to a success page or the newly created experience
        return redirect("vendor:vendor_list")

    else:
        # Get all category choices from the model for the dropdown
        categories = Experience.CATEGORY_CHOICES

    return render(request, 'vendor/host.html', {
        'categories': categories
    })
# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from base.models import CustomUser

@login_required(login_url='signin')
def form(request):
    user = request.user

    if request.method == 'POST':
        # Get form data
        phone_number = request.POST.get('phone_number')
        business_name = request.POST.get('business_name')
        vendor_type = request.POST.get('vendor_type')
        is_agreed = request.POST.get('is_agreed') == 'on'  # Check if the checkbox is checked

        # Update the user fields
        user.phone_number = phone_number
        user.business_name = business_name
        user.vendor_type = vendor_type
        user.is_agreed = is_agreed
        user.role= 'vendor'
        user.is_vendor = True

        # Save the user profile
        user.save()
        Notification.objects.create(user=user,message =f'{user.username} became a new vendor')

        # Redirect to some success page or back to the profile page
        return redirect('vendor:congrat')

    # Render the form with current user data
    return render(request, 'vendor/form.html', {
        'user': user,
    })
def congrat(request):
    return render (request, 'vendor/congrat.html')
def dashboard(request):
    experience_number = Experience.objects.filter(vendor__user=request.user).count()
    latest_experiences = Experience.objects.filter(vendor__user=request.user).order_by('-created_at')[:2]
    
    context = {
        'experience_number':experience_number,
        'latest_experiences':latest_experiences
    }
    return render (request, 'vendor/dashboard.html',context)

def earn(request):
    return render (request, 'vendor/earn.html')

def vendor_list(request):
    list = Experience.objects.filter(vendor__user=request.user)
    context = {
        'list':list
    }
    return render(request, 'vendor/vendor-list.html',context)

from base.models import *
def payment(request):
    if request.method == "POST":
        paypal_email = request.POST.get('paypal_email')

        Vendorpaypal.objects.create(paypal_email =paypal_email ,user =request.user)
        return redirect('vendor:payment')

    return render (request, 'vendor/payment.html')


def vendor_edit(request,title):
    if Experience.objects.filter(vendor__user=request.user).exists():
        edit = get_object_or_404(Experience,title=title,vendor__user=request.user)
        if request.method == "POST":
            title = request.POST.get('title')
            description = request.POST.get('description')
            category = request.POST.get('category')
            location = request.POST.get('location')
            price = request.POST.get('price')
            available_slots = request.POST.get('available_slots')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            tags = request.POST.get('tags')
            duration = request.POST.get('duration')
            requirements = request.POST.get('requirements')
            what_to_bring = request.POST.get('what_to_bring')
            images = request.FILES.get('images')

            edit.title =title
            edit.description =description
            edit.category =category
            edit.location =location
            edit.price =price
            edit.available_slots =available_slots
            edit.start_date =start_date
            edit.end_date =end_date
            edit.tags =tags
            edit.duration =duration
            edit.requirements =requirements
            edit.what_to_bring =what_to_bring
            edit.images =images

            edit.save()
            messages.success(request, 'Saved Successfully')
            return redirect('vendor:vendor_edit',title=title)
        print(edit.category)
        categories = Experience.CATEGORY_CHOICES
        context = {
            'edit':edit,
            'categories':categories
        }

        return render (request, 'vendor/vendor-edit.html',context)
    
def delete_expricence(request,pk):
     if Experience.objects.filter(vendor__user=request.user).exists():
         dek = get_object_or_404(Experience,pk=pk,vendor__user=request.user)
         dek.delete()
         return redirect('vendor:vendor_list')

