from django.urls import path
from . import views
from .views import chat_view
urlpatterns = [
    path('',views.index,name="index"),
    path('signup',views.signup,name="signup"),
    path('signin',views.signin,name="signin"),
    path('logout',views.logout,name="logout"),
    path('watch',views.watch,name="watch"),
    path('verify',views.verify_code,name="verify"),
    path('profile',views.userprofile,name="profile"),
    path('privacy',views.privacy,name="privacy"),
    path('search',views.search,name="search"),
    path('experience/<int:pk>/',views.experience,name="experience"),
    path('experience/<int:id>/payment/', views.experience_payment, name='experience_payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('contact',views.contact,name="contact"),
    path('about',views.about,name="about"),
    path('faq',views.faq,name="faq"),
    path('add-to-watchlist/<int:experience_id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('remove-from-watchlist/<int:experience_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('view-watchlist/', views.view_watchlist, name='view_watchlist'),
    path('count-watchlist/', views.countwatch, name='count_watchlist'),
    path('api/cart/status/<int:experience_id>/', views.cart_status, name='cart_status'),
    path('create-payment/<int:experience_id>/', views.create_paypal_order, name='create_paypal_order'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
    path('chat/<int:experience_id>/', chat_view, name='chat'),
    path('update-status/', views.update_status, name='update_status'),
    

    
 
]
