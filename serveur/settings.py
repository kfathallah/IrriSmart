#python manage.py runserver --insecure

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY='c-8!(4py=15$#+@ihvznp%wo892e9-9hu%3rwdd0(4=50r_kr@'

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG=True

# Admins will get error/exception mails

ADMINS=[
    ('bennouri iheb', 'bennouri.iheb@gmail.com'),
    ('hamdi alaa mohamed', 'hamdi.med.alaa@gmail.com')
]

MANAGERS=ADMINS

ALLOWED_HOSTS=['*']

# Application definition

INSTALLED_APPS=[
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'application'
]

MIDDLEWARE=[
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'application.middleware.Controlleur',
]

ROOT_URLCONF='serveur.urls'

TEMPLATES=[
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'serveur.wsgi.application'

# Database

DATABASES={
    'default' : {
        'ENGINE' : 'django.contrib.gis.db.backends.postgis',
        'NAME': 'postgisDB',
        'USER' : 'postgres',
        'PASSWORD' : 'root',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}

# Password validation

AUTH_PASSWORD_VALIDATORS=[
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

LANGUAGE_CODE='en-us'

TIME_ZONE='Africa/Tunis'

USE_I18N=True

USE_L10N=True

USE_TZ=True

# Static files (CSS, JavaScript, Images)

STATIC_URL='/static/'

MEDIA_URL='/media/'

MEDIA_ROOT=os.path.join(BASE_DIR, 'media')

FILE_UPLOAD_HANDLERS=[
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler"
]

SERIALIZATION_MODULES={
    "geojson": "django.contrib.gis.serializers.geojson", 
}

# Mail settings

EMAIL_HOST='localhost'

EMAIL_PORT=1025
