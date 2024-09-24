from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name="index"),
    path('signup',views.signup,name="signup"),
    path('signin',views.signin,name="signin"),
    path('logout',views.logout,name="logout"),
    path('verify',views.verify_code,name="verify"),
    path('profile',views.userprofile,name="profile"),
    path('privacy',views.privacy,name="privacy"),
    path('experience/<int:pk>/',views.experience,name="experience"),
    path('experience/<int:id>/payment/', views.experience_payment, name='experience_payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('contact',views.contact,name="contact"),
    path('about',views.about,name="about"),
    path('add-to-watchlist/<int:experience_id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('remove-from-watchlist/<int:experience_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('watchlist/', views.view_watchlist, name='view_watchlist'),

    
 
]
