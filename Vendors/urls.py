from django.urls import path
from Vendors import views
app_name = 'Vendors'


urlpatterns = [
    path('signup',views.signup,name="signup"),
    path('signup-vendor',views.signup_vendor,name= "signup-vendor"),
    path('login',views.login,name="login"),
    path('host',views.create_experience,name="host"),
    path('form',views.form,name="form"),
    path('congrat',views.congrat,name="congrat"),
    path('dashboard',views.dashboard,name="dashboard"),
]
