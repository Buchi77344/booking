
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    # Common fields
    
    
    # Vendor-specific fields
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    business_name = models.CharField(max_length=255, null=True, blank=True)
    vendor_type = models.CharField(max_length=20, choices=[('individual', 'Individual'), ('small_business', 'Small Business'), ('organization', 'Organization')], null=True, blank=True)
    verification_code = models.CharField(max_length=6, blank=True, null=True)  # Store the verification code
    is_verified = models.BooleanField(default=False) 
    is_agreed = models.BooleanField(default=False) 
    is_vendor  = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False) 
    date_birth =models.DateField( null=True)
    
    # Other fields
    role = models.CharField(max_length=10, choices=[('user', 'User'), ('vendor', 'Vendor')], default='user')

    def __str__(self):
        return self.username
from django_countries.fields import CountryField
from django.db.models.signals import post_save
from django.dispatch import receiver

class Userprofile(models.Model):
   profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
   user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='userprofile')
   phone_number = models.CharField(max_length=15, null=True, blank=True)
   country = CountryField(blank_label='(select country)', null=True, blank=True)
   street_address = models.CharField(max_length=255, null=True, blank=True)
   city = models.CharField(max_length=255, null=True, blank=True)
   zipcode = models.CharField(max_length=255, null=True, blank=True)
   def __str__(self):
        return f' {self.user.username} Profile'

import requests
from django.core.files.base import ContentFile
from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.socialaccount.models import SocialAccount
from .models import Userprofile, CustomUser

def download_image(url):
    """Download image from a URL and return the ContentFile."""
    response = requests.get(url)
    if response.status_code == 200:
        return ContentFile(response.content)
    return None

@receiver(post_save, sender=CustomUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if instance.role == 'user':
        # Create or get the user profile
        user_profile, created = Userprofile.objects.get_or_create(user=instance)

        # Check if the user signed up using Google
        social_account = SocialAccount.objects.filter(user=instance, provider='google').first()

        if social_account:
            # Extract relevant Google data from the extra_data field
            extra_data = social_account.extra_data
            google_picture_url = extra_data.get("picture")

            # Download the image and save it to the profile_picture field
            if google_picture_url and not user_profile.profile_picture:
                image_content = download_image(google_picture_url)
                if image_content:
                    user_profile.profile_picture.save(f'{instance.username}_profile.jpg', image_content, save=True)

        # Save the user profile if it was created or updated
        user_profile.save()


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.role == 'user':
        instance.userprofile.save()
    
class VendorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='vendor_profile')
    bio = models.TextField(blank=True, null=True)
    verification_documents = models.FileField(upload_to='documents/', blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.email

def save_user_model(sender ,instance,created,**kwargs):
    if created:
          VendorProfile.objects.create(user=instance)
  

post_save.connect(save_user_model, sender=CustomUser )


class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    experience = models.ForeignKey('Experience', on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()  # 1 to 5 rating system
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.experience.title}"
    


# Experience Categories (e.g., Tours, Workshops, etc.)
from django.db import models

class ExperienceCategory(models.Model):
    CATEGORY_CHOICES = [
        ('adventure_outdoor', 'Adventure & Outdoor'),
        ('cultural_historical', 'Cultural & Historical'),
        ('food_drink', 'Food & Drink'),
        ('wellness_relaxation', 'Wellness & Relaxation'),
        ('entertainment_shows', 'Entertainment & Shows'),
        ('workshops_learning', 'Workshops & Learning'),
        ('nature_wildlife', 'Nature & Wildlife'),
        ('water_activities', 'Water Activities'),
        ('romantic_special', 'Romantic & Special Occasions'),
        ('family_friendly', 'Family-Friendly'),
        ('luxury_experiences', 'Luxury Experiences'),
        ('seasonal_holiday', 'Seasonal & Holiday'),
    ]
    
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.get_name_display()  # Display human-readable name


    def __str__(self):
        return self.name

# Experience Model (Offered by Vendors)
from django.db import models

from django.db import models
class Experience(models.Model):
    CATEGORY_CHOICES = [
        ('adventure_outdoor', 'Adventure & Outdoor'),
        ('cultural_historical', 'Cultural & Historical'),
        ('food_drink', 'Food & Drink'),
        ('wellness_relaxation', 'Wellness & Relaxation'),
        ('entertainment_shows', 'Entertainment & Shows'),
        ('workshops_learning', 'Workshops & Learning'),
        ('nature_wildlife', 'Nature & Wildlife'),
        ('water_activities', 'Water Activities'),
        ('romantic_special', 'Romantic & Special Occasions'),
        ('family_friendly', 'Family-Friendly'),
        ('luxury_experiences', 'Luxury Experiences'),
        ('seasonal_holiday', 'Seasonal & Holiday'),
    ]

    # Basic fields
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    location = models.CharField(max_length=255)

    # Pricing fields
    # Base price
    private_group_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Price for private groups
    price_per_guest = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Price per guest
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Discount price (if applicable)

    # Availability fields
    available_slots = models.IntegerField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()

    # Guest settings
    min_guests = models.PositiveIntegerField(default=1)  # Minimum number of guests
    max_guests = models.PositiveIntegerField(default=20)  # Maximum number of guests

    # Session details
    calendar_view = models.JSONField(blank=True, null=True)  # To store session details and dates in JSON format
    sessions_per_day = models.PositiveIntegerField(default=1)  # Number of sessions per day

    # Creation and update timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Relationships
    vendor = models.ForeignKey('VendorProfile', on_delete=models.CASCADE, related_name='experiences')
    vendor_user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, null=True)

    # Additional fields for guest and experience details
    guest = models.IntegerField(default=0)
    images = models.ImageField(upload_to='experience_images/', null=True, blank=True)  # Image upload
    tags = models.CharField(max_length=255, blank=True)  # Comma-separated tags for searching/filtering
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)  # Average rating
    is_featured = models.BooleanField(default=False)  # Flag for featured experiences
    duration = models.CharField(max_length=50)  # Duration of the experience (e.g., "3 hours", "2 days")
    requirements = models.TextField(blank=True)  # Any special requirements (age limits, physical fitness, etc.)
    what_to_bring = models.TextField(blank=True)  # A list of recommended things to bring

    # Payment information
    paypal = models.ForeignKey('Vendorpaypal', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.title} by"



# Booking Model (Users booking an experience from a Vendor)
class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(default=timezone.now)
    number_of_people = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Booking by {self.user.username} for {self.experience.title}"

from django.db import models

from .models import Experience

class Transaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=255)  # Razorpay Order ID
    payment_id = models.CharField(max_length=255)  # Razorpay Payment ID
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Transaction {self.order_id} for {self.experience.title}"

class Watchlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='watchlist')
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='in_watchlist')
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.experience.title}'
    

class Vendorpaypal(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    paypal_email =models.EmailField(max_length=254)

    def __str__(self):
        return self.paypal_email
    
class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(null=True, max_length=50)
    message =models.CharField( max_length=50,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True) 




# models.py
# models.py
from django.db import models
from django.contrib.auth import get_user_model


class ChatMessage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='messages',null =True)
    vendor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='vendor_messages',null =True)
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='chat_messages',null =True)  # Foreign key to Experience
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.user.username} to {self.vendor.username}: {self.message}'



 