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
    return render (request, 'vendor/group-pr.html')
def what_do(request):
    return render (request, 'vendor/theme-form.html')
def description(request):
    return render (request, 'vendor/activities-form.html')
def over(request):
    return render (request, 'vendor/overview-form.html')
def group_size(request):
    return render (request, 'vendor/groupsz-form.html')
def booking_st(request):
    return render (request, 'vendor/booking-st.html')
def cancel(request):
    return render (request, 'vendor/cancelllation-pl.html')
def general(request):
    return render (request, 'vendor/general-avail.html')
def title(request):
    return render (request, 'vendor/title-form.html')
def image(request):
    return render (request, 'vendor/image-upload.html')


@login_required(login_url='signin')
def create_experience(request):
    if request.method == 'POST':
        # Retrieve form data
        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('category')
        location = request.POST.get('location')
        private_group_price = request.POST.get('private_group_price')
        private_group_max_guests = request.POST.get('private_group_max_guests')  # New field for max guests in private group
        price_per_guest = request.POST.get('price_per_guest')
        available_slots = request.POST.get('available_slots')
        tags = request.POST.get('tags')
        duration = request.POST.get('duration')
        requirements = request.POST.get('requirements')
        what_to_bring = request.POST.get('what_to_bring')
        images = request.FILES.get('images')
        videos = request.FILES.get('videos')  # Video upload
        min_guests = request.POST.get('min_guests')
        max_guests = request.POST.get('max_guests')
        calendar_view = request.POST.get('calendar_view')

        # Process extra services
        extra_services = []
        service_count = 1
        while True:
            service_name = request.POST.get(f'extra_service_name_{service_count}')
            service_price = request.POST.get(f'extra_service_price_{service_count}')
            if not service_name or not service_price:
                break
            extra_services.append({
                'name': service_name,
                'price': service_price
            })
            service_count += 1

        # Retrieve the vendor profile and ensure the vendor has a PayPal account
        vendor_profile = get_object_or_404(VendorProfile, user=request.user)
        vendor_user = get_object_or_404(Userprofile, user=request.user)
        vendor_paypal_instance = get_object_or_404(Vendorpaypal, user=request.user)

        # Create the Experience instance
        new_experience = Experience.objects.create(
            title=title,
            description=description,
            category=category,
            location=location,
            private_group_price=private_group_price,
            price_per_guest=price_per_guest,
            available_slots=available_slots,
            vendor=vendor_profile,
            paypal=vendor_paypal_instance,
            vendor_user=vendor_user,
            tags=tags,
            duration=duration,
            requirements=requirements,
            what_to_bring=what_to_bring,
            images=images,
            min_guests=min_guests,
            max_guests=max_guests,
            calendar_view=calendar_view,
        )

        # Save extra services to the experience (you may want to save it as a JSON field or related model)
        new_experience.extra_services = extra_services  # Assuming extra_services is a JSONField in the Experience model
        new_experience.save()

        # Handle video upload
        if videos:
            new_experience.videos = videos
            new_experience.save()

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
        'paypal':paypal
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
