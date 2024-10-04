from django.shortcuts import render
from base.models import *
from django.db.models import *

# Create your views here.

def dashboard(request):
    total_user = CustomUser.objects.all().count()
    total_vendor =CustomUser.objects.filter(role='vendor').count()
    total_experience = Experience.objects.all().count()
    total_revenue = Transaction.objects.aggregate(Sum('amount'))['amount__sum'] or 0 
    notification =Notification.objects.all().order_by('-created_at')[:5]
    context ={
        'total_user':total_user, 
        'total_vendor':total_vendor,
        'total_experience':total_experience,
        'total_revenue':total_revenue,
        'notification':notification,
    }
    return render (request, 'admin/dashboard.html',context)

def experience(request):
    exp = Experience.objects.all()
    context ={
        'exp':exp
    }
    return render (request, 'admin/experience.html',context)

def user_management(request):
    user = CustomUser.objects.all()
    context ={
        'user':user
    }
    return render (request, 'admin/user_management.html',context)

def vendor_management(request):
    vendor = CustomUser.objects.filter(role='vendor')
    context = {
        'vendor':vendor
    }
    return render (request, 'admin/vendor_management.html',context)
def view_transactons(request):
    trac = Transaction.objects.all()
    context = {
        'trac':trac
    }
    return render (request, 'admin/view_transactions.html',context)

def view_reviews(request):
    return render (request, 'admin/view_reviews.html')

def settings(request):
    return render (request, 'admin/settings.html')