from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name="index"),
    path('signup',views.signup,name="signup"),
    path('signin',views.signin,name="signin"),
    path('verify',views.verify_code,name="verify"),
    path('profile',views.userprofile,name="profile"),
    path('privacy',views.privacy,name="privacy"),
    path('experience/<int:pk>/',views.experience,name="experience"),
    path('experience/<int:id>/payment/', views.experience_payment, name='experience_payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
    
 
]
