
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Common fields
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    
    # Vendor-specific fields
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    business_name = models.CharField(max_length=255, null=True, blank=True)
    vendor_type = models.CharField(max_length=20, choices=[('individual', 'Individual'), ('small_business', 'Small Business'), ('organization', 'Organization')], null=True, blank=True)
    verification_code = models.CharField(max_length=6, blank=True, null=True)  # Store the verification code
    is_verified = models.BooleanField(default=False) 
    
    # Other fields
    role = models.CharField(max_length=10, choices=[('user', 'User'), ('vendor', 'Vendor')], default='user')

    def __str__(self):
        return self.username
    
class VendorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='vendor_profile')
    bio = models.TextField(blank=True, null=True)
    verification_documents = models.FileField(upload_to='documents/', blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.email
