
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
        return f' Profile'

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'user':
        Userprofile.objects.create(user=instance)

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


class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    experience = models.ForeignKey('Experience', on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()  # 1 to 5 rating system
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.experience.title}"
    


# Experience Categories (e.g., Tours, Workshops, etc.)
class ExperienceCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# Experience Model (Offered by Vendors)
class Experience(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(ExperienceCategory, on_delete=models.CASCADE, related_name='experiences')
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_slots = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name='experiences')
    
    # Additional fields
    images = models.ImageField(upload_to='experience_images/', null=True, blank=True)  # Image upload
    tags = models.CharField(max_length=255, blank=True)  # Comma-separated tags for searching/filtering
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)  # Average rating
    is_featured = models.BooleanField(default=False)  # Flag for featured experiences
    duration = models.CharField(max_length=50)  # Duration of the experience (e.g., "3 hours", "2 days")
    requirements = models.TextField(blank=True)  # Any special requirements (age limits, physical fitness, etc.)
    what_to_bring = models.TextField(blank=True)  # A list of recommended things to bring
    
    def __str__(self):
        return f"{self.title} by {self.vendor.business_name}"

# Booking Model (Users booking an experience from a Vendor)
class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(default=timezone.now)
    number_of_people = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Booking by {self.user.username} for {self.experience.title}"

