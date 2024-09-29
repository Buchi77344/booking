"""
Django settings for booking project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-b$@equ&jmrd$9xb5=0yg*d5q&enqdwo08nss3zv&88yd(7#8cr'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
  

# Application definition

INSTALLED_APPS = [
    'django.contrib.sites',  # Required by Allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'base',
    'Vendors',
    'Experiences', 
    'django_countries',
   
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware', 
]

ROOT_URLCONF = 'booking.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR,'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'booking.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Required for Django Allauth
SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',  # Allauth authentication backend
)



SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '735819647020-i2okdjtvpo7lgacunmjd4pq2e8or4pg5.apps.googleusercontent.com'  # Client ID
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'  # Client Secret


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILE = [
    os.path.join(BASE_DIR, 'static')
]
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR / 'media')
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL = 'base.CustomUser'







# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'experiencehotspot@gmail.com'
# EMAIL_HOST_PASSWORD = 'jkqvaafqvinxwdwu'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_PORT = 587  # Use 465 if you're using SSL
EMAIL_USE_TLS = True  # Set to True for TLS
EMAIL_HOST_USER = 'experiencehotspot@zohomail.com'  # Your Zoho email address
EMAIL_HOST_PASSWORD = 'BsBUiZ6A0LrW'


ADMIN_EMAIL = 'experiencehotspot@gmail.com'

SITE_NAME= "Experience Hotspot"

# clint id = '735819647020-i2okdjtvpo7lgacunmjd4pq2e8or4pg5.apps.googleusercontent.com'



# c;int secret ='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'
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APPS": [
            {
                "client_id": "735819647020-i2okdjtvpo7lgacunmjd4pq2e8or4pg5.apps.googleusercontent.com",
                "secret": "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",
            },
        ],
        "SCOPE": [
            "profile",  # This scope includes the user's name and picture.
            "email",    # This scope includes the user's email address.
        ],
        "FIELDS": [
            "id",
            "email",
            "name",
            "given_name",     # Google's equivalent to first name
            "family_name",    # Google's equivalent to last name
            "picture",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    },
    "facebook": {
        # Facebook OAuth settings
        "APPS": [
            {
                "client_id": "493367440210309", 
                "secret": "3dd45b7381c63940c1baff34a78b162c",
            },
        ],
        "SCOPE": [
            "email",
            "public_profile",
        ],
        "FIELDS": [
            "id",
            "email",
            "name",
            "first_name",
            "last_name",
            "picture",
        ],
        "AUTH_PARAMS": {
            "auth_type": "reauthenticate"
        },
    },
}

SOCIALACCOUNT_LOGIN_ON_GET = True
LOGIN_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = '/'  # Redirect to home page after login
ACCOUNT_SIGNUP_REDIRECT_URL = '/'  # Redirect after signup
LOGOUT_REDIRECT_URL = '/'  # Redirect after logout
ACCOUNT_LOGOUT_ON_GET = True 



RAZORPAY_KEY_ID = 'rzp_live_JShwqIsgcWWsNp'
RAZORPAY_KEY_SECRET = 'yElAwSsRLV9QbtvOfPOixOTC'


ACCOUNT_ADAPTER = 'allauth.account.adapter.DefaultAccountAdapter'
SOCIALACCOUNT_ADAPTER = 'allauth.socialaccount.adapter.DefaultSocialAccountAdapter'



