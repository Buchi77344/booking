from django.contrib import admin

# Register your models here.
from .models import *
 
admin.site.register(CustomUser)
admin.site.register(Userprofile)
admin.site.register(VendorProfile)
admin.site.register(ExperienceCategory)
admin.site.register(Experience)
admin.site.register(Review) 
admin.site.register(Transaction) 
admin.site.register(Watchlist)
admin.site.register(Vendorpaypal)