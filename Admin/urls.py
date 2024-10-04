from django.urls import path
from Admin import views

app_name="Admin"

urlpatterns = [
    path('dashboard',views.dashboard,name="dashboard"),
    path('experience',views.experience,name="experience"),
    path('user_management',views.user_management,name="user_management"),
    path('vendor_management',views.vendor_management,name="vendor_management"),
    path('view_transactons',views.view_transactons,name="view_transactons"),
    path('view_reviews',views.view_reviews,name="view_reviews"),
    path('settings',views.settings,name="settings"),
]
