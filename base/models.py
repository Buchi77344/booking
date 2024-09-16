
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
    vendor_bio = models.TextField(null=True, blank=True)
    verification_document = models.FileField(upload_to='verification_docs/', null=True, blank=True)
    
    # Other fields
    role = models.CharField(max_length=10, choices=[('user', 'User'), ('vendor', 'Vendor')], default='user')

    def __str__(self):
        return self.username
