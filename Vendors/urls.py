from django.urls import path
from Vendors import views
app_name = 'Vendors'


urlpatterns = [
    path('signup',views.signup,name="signup"),
    path('signup-vendor',views.signup_vendor,name= "signup-vendor"),
    path('login',views.login,name="login"),
]
