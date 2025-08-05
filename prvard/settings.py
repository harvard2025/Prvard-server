"""
Django settings for prvard project.
"""


import os
from pathlib import Path
from dotenv import load_dotenv

# 1) عرّف BASE_DIR أولاً
BASE_DIR = Path(__file__).resolve().parent.parent

# 2) حمّل متغيّرات البيئة من env.env
load_dotenv(BASE_DIR / 'env.env')


# 3) الآن يمكنك استخدام os.getenv() بأمان
SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret')
DEBUG = os.getenv('DEBUG', 'True') == 'True'




ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.onrender.com',  # Allow all Render subdomains
    'prvard.onrender.com',  # Your Render URL
    'prvard.ddns.net',  # Your No-IP domain
    'www.prvard.ddns.net',
    'harvard.ddns.net',            # Your No-IP domain
    'www.harvard.ddns.net',    
]

# Application definition
INSTALLED_APPS = [
    'prvard_main',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary',
    'cloudinary_storage',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add WhiteNoise
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'prvard.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'prvard.wsgi.application'

# Database
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Additional static files directories
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'prvard_main', 'static'),
]

# WhiteNoise configuration for static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Security settings for production
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    
    
    
    

    
    
    
# Add this to the END of your settings.py file

import os
from django.core.management import execute_from_command_line

def create_superuser():
    """Create superuser if it doesn't exist"""
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Define superuser credentials
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123456')
        
        # Check if superuser exists
        if not User.objects.filter(username=username).exists():
            print(f"Creating superuser: {username}")
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            print("Superuser created successfully!")
        else:
            print(f"Superuser '{username}' already exists")
            
    except Exception as e:
        print(f"Error creating superuser: {e}")

# Only run this in production (on Render)
if os.environ.get('RENDER'):
    # Import Django and setup
    import django
    django.setup()
    
    # Create superuser after Django is ready
    try:
        create_superuser()
    except:
        pass  # Ignore errors during startup
        
        
    
    
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY':    os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}

# اجعل Django يستخدم Cloudinary لتخزين الملفات المرفوعة
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    
