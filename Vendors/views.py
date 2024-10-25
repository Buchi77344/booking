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
from base.models import *
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
from django.contrib.auth.decorators import login_required




def group_price(request):
     if request.method == "POST":
        price_per_guest = request.POST.get('price_per_guest')
        private_group_price = request.POST.get('private_group_price')
        request.session['price_per_guest']= price_per_guest
        request.session['private_group_price']= private_group_price
        return redirect('vendor:booking_st')
     return render (request, 'vendor/group-pr.html')
def what_do(request):
    return render (request, 'vendor/theme-form.html')
def description(request):
    if request.method == "POST":
        description = request.POST.get('description')
        duration = request.POST.get('duration')

        request.session['description']= description
        request.session['duration']= duration
        print(description, duration)
        return redirect('vendor:general')

    return render (request, 'vendor/activities-form.html')
def over(request):
    return render (request, 'vendor/overview-form.html')
def group_size(request):
     if request.method == "POST":
         public_size = request.POST.get('public_size')
         private_size = request.POST.get('private_size')
         
         request.session['public_size']= public_size
         request.session['private_size']= private_size
         return redirect('vendor:group_price')
     return render (request, 'vendor/groupsz-form.html')
def booking_st(request):
    if request.method == "POST":
         cut = request.POST.get('cut')
         cut1 = request.POST.get('cut1')
         return redirect('vendor:cancel')
    return render (request, 'vendor/booking-st.html')

def cancel(request):
    if request.method == "POST":
        # Check if all required session keys are present
        required_fields = [
            'location', 'category', 'file_name', 'title', 'calendar_view', 
            'start_time', 'end_time', 'price_per_guest', 'private_group_price', 
            'description', 'duration', 'public_size', 'private_size'
        ]

        missing_fields = [field for field in required_fields if not request.session.get(field)]
        
        if missing_fields:
            # If any required fields are missing, redirect to index with a message
            messages.warning(request, "Some session data is missing.")
            return redirect('vendor:host')

        # Extract session data if all required fields are present
        experience_data = {field: request.session.get(field) for field in required_fields}

        # Create the Experience object
        experience, created = Experience.objects.get_or_create(**experience_data)

        return redirect('vendor:vendor_list')

    return render(request, 'vendor/cancelllation-pl.html')
def general(request):
    if request.method == 'POST':
        calendar_view =request.POST.get('calendar_view')
        start_time = request.POST.get('start_time')
        end_time =request.POST.get('end_time')

        request.session['calendar_view']=calendar_view
        request.session['start_time']=start_time
        request.session['end_time']=end_time
        return redirect('vendor:group_price')
        
    return render (request, 'vendor/general-avail.html')
def title(request):
    if request.method == 'POST':
        title =request.POST.get('title')
        request.session['title']=title
        return redirect('vendor:image')
    return render (request, 'vendor/title-form.html')
import os
from django.conf import settings
from django.core.files.storage import default_storage
def image(request):
    if  request.method == 'POST':
        images = request.FILES.get('images')
        file_path = os.path.join('experience_images', images.name)

        # Save the file to the specified directory in 'MEDIA_ROOT/image/'
        file_name = default_storage.save(file_path, images)

        # Store the file path in the session
        request.session['file_name'] = file_name
        print(file_name)
        return redirect('vendor:description')
    return render (request, 'vendor/image-upload.html')


@login_required(login_url='signin')
def create_experience(request):
    if request.method == 'POST':
        location = request.POST.get('location')
        category =request.POST.get('category')

        request.session['location']=location
        request.session['category']=category
        return redirect('vendor:title')
       
    categories = Experience.CATEGORY_CHOICES
    context = {
        'categories':categories
    }

  
    return render(request, 'vendor/host.html', context
       
    )


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
@login_required(login_url='signin')
def dashboard(request):
    user = request.user
    vendor_profile = VendorProfile.objects.get(user=user)
    # if Vendorpaypal.objects.filter(user=user).exists():

    #     paypal = Vendorpaypal.objects.get(user=user)

        # Get all experiences hosted by this vendor
    vendor_experiences = Experience.objects.filter(vendor=vendor_profile)

        # Get all paid transactions related to those experiences
    transactions = Transaction.objects.filter(experience__in=vendor_experiences, is_paid=True)

        # Calculate total earnings by summing up the amounts of those transactions
    total_earnings = transactions.aggregate(Sum('amount'))['amount__sum'] or 0
    experience_number = Experience.objects.filter(vendor__user=request.user).count()
    latest_experiences = Experience.objects.filter(vendor__user=request.user).order_by('-created_at')[:2]
    
    context = {
        'experience_number':experience_number,
        'latest_experiences':latest_experiences,
        'total_earnings':total_earnings,
        
    }
    return render (request, 'vendor/dashboard.html',context)
from django.db.models import *

@login_required(login_url='signin')
def earn(request):
    # Assuming the logged-in user is a CustomUser with a related VendorProfile
    user = request.user
    
    try:
        # Retrieve the VendorProfile instance associated with the user
        vendor_profile = VendorProfile.objects.get(user=user)

        # Get all experiences hosted by this vendor
        vendor_experiences = Experience.objects.filter(vendor=vendor_profile)

        # Get all paid transactions related to those experiences
        transactions = Transaction.objects.filter(experience__in=vendor_experiences, is_paid=True)

        # Calculate total earnings by summing up the amounts of those transactions
        total_earnings = transactions.aggregate(Sum('amount'))['amount__sum'] or 0

    except VendorProfile.DoesNotExist:
        # Handle case where the user does not have a VendorProfile
        vendor_experiences = []
        transactions = []
        total_earnings = 0

    # Pass transactions and total earnings to the template
    return render(request, 'vendor/earn.html', {
        'transactions': transactions,
        'total_earnings': total_earnings
    })
   
@login_required(login_url='signin')
def vendor_list(request):
    list = Experience.objects.filter(vendor__user=request.user)
    context = {
        'list':list
    }
    return render(request, 'vendor/vendor-list.html',context)

from base.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render
 # Adjust the import as necessary

@login_required(login_url='signin')
def payment(request):
    if request.method == "POST":
        paypal_email = request.POST.get('paypal_email')

        # Get or update the Vendorpaypal instance for the current user
        vendor_paypal_instance, created = Vendorpaypal.objects.get_or_create(user=request.user)

        # Update the PayPal email
        vendor_paypal_instance.paypal_email = paypal_email
        vendor_paypal_instance.save()

        if created:
            messages.success(request, 'Your PayPal email has been added successfully.')
        else:
            messages.success(request, 'Your PayPal email has been updated successfully.')

        return redirect('vendor:payment')

    return render(request, 'vendor/payment.html')


@login_required(login_url='signin')
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
@login_required(login_url='signin')
def delete_expricence(request,pk):
     if Experience.objects.filter(vendor__user=request.user).exists():
         dek = get_object_or_404(Experience,pk=pk,vendor__user=request.user)
         dek.delete()
         return redirect('vendor:vendor_list')
     



from django.db.models import Max

from base.models import Experience  # Assuming Experience model is in base app

def vendorchat(request):
    # Get messages where the user is the vendor
    messages = ChatMessage.objects.filter(vendor=request.user)

    # Get the latest message for each user who messaged the vendor
    latest_messages = messages.values('user').annotate(
        last_message_time=Max('timestamp')
    ).order_by('-last_message_time')

    # Get all users who messaged the vendor with their last message content
    users = []
    for message in latest_messages:
        # Get the user who sent the last message
        chat_message = ChatMessage.objects.get(
            user=message['user'],
            vendor=request.user,
            timestamp=message['last_message_time']
        )
        
        # Fetch the last message content
        last_message = chat_message.message
        
        # Get the experience associated with the chat message
        experience = chat_message.experience  # Assuming ChatMessage has an experience field

        users.append({
            'username': chat_message.user.username,
            'user_id': chat_message.user.id, 
            'last_message': last_message,  # Get the message content
            'last_message_time': message['last_message_time'],  # Optionally show the time too
            'experience_id': experience.id  # Pass the experience id
        })

    return render(request, 'vendor/vendor_chat_list.html', {'users': users})
