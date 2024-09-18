from django.contrib import admin

# Register your models here.
from .models import CustomUser,Userprofile ,VendorProfile,ExperienceCategory,Experience,Review
 
admin.site.register(CustomUser)
admin.site.register(Userprofile)
admin.site.register(VendorProfile)
admin.site.register(ExperienceCategory)
admin.site.register(Experience)
admin.site.register(Review) 