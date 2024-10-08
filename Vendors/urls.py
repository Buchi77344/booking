from django.urls import path
from Vendors import views
from  Vendors.views import *
app_name = 'Vendors'


urlpatterns = [
    path('signup',views.signup,name="signup"),
    path('signup-vendor',views.signup_vendor,name= "signup-vendor"),
    path('login',views.login,name="login"),
    path('host',views.create_experience,name="host"),
    path('form',views.form,name="form"),
    path('congrat',views.congrat,name="congrat"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('earn',views.earn,name="earn"),
    path('vendor_list',views.vendor_list,name="vendor_list"),
    path('payment',views.payment,name="payment"),
    path('vendor_edit/<str:title>/',views.vendor_edit,name="vendor_edit"),
    path('delete_expricence/<int:pk>/',views.delete_expricence,name="delete_expricence"),
    path('vendorchat', vendorchat, name='vendorchat'), 
  
]
