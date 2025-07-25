"""
Django settings for webproject project.

Generated by 'django-admin startproject' using Django 5.0.4.

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
SECRET_KEY = 'django-insecure-k)(2m9-h!*ovms9*sh!t5)5+5tn#v@f)f)98cws-#c=7y3w@u9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost','127.0.0.1','202.29.55.222','greenlibrary.npu.ac.th','f6cc27685e2b.ngrok-free.app','10.104.51.133']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'greenweb',
    'indexweb',
    'category',
    'blogs',
    'admin_reorder',
    'docChecker',
    'info_graph',
    'promotional',
    'resources',
    'django_filters',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'admin_reorder.middleware.ModelAdminReorder',
]

# อนุญาตให้เว็บไซต์สามารถถูกโหลดใน iframe จากโดเมนเดียวกันได้
X_FRAME_OPTIONS = 'SAMEORIGIN'

ROOT_URLCONF = 'webproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'webproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'greenlibrary',
        'USER': 'root',
        'PASSWORD': '',
        'HOST':'localhost',
        'POER':'3306',
        'OPTIONS':{
            'charset':'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION'",
        }
    }
}

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        'NAME': 'greenlibrary',
#        'USER': 'root',
#        'PASSWORD': '',
#        'HOST':'127.0.0.1',
#        'POER':'3306',
#        'OPTIONS':{
#            'charset':'utf8mb4',
#            'init_command': "SET sql_mode='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION'",
#        }
#    }
#}


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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'attachments/')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Admin reorder
ADMIN_REORDER = (
    {
        'app': 'auth',
        'label': 'Authentication and Authorization',
        'models': [
            {'model': 'auth.User', 'label': 'Users'},
            {'model': 'auth.Group', 'label': 'Groups'},
        ]
    },
    {
        'app': 'category',
        'label': 'Category',
        'models': [
        'category.Category',
        ]
    },
    {
        'app': 'greenweb',
        'models': [
            'greenweb.Year',
            'greenweb.Category',
            'greenweb.Issue',
            'greenweb.Indicator',
            'greenweb.Evidence',
        ]
    },
    {
        'app': 'docChecker',
        'models': [
            'docChecker.Year',
            'docChecker.CategoryGroup',
            'docChecker.Category',
            'docChecker.Issue',
            'docChecker.Indicator',
            'docChecker.Evidence',
        ]
    },
    {
        'app': 'info_graph',
        'models': [
            'info_graph.Year',
            'info_graph.Month',
            'info_graph.DataEntry',
        ]
    },
    {
        'app': 'promotional',
        'label': 'สื่อประชาสัมพันธ์',
        'models': [
            'promotional.PromotionalCategory',
            'promotional.PromotionalImage',
        ]
    },
    # ใส่แอปพลิเคชันและโมเดลตามลำดับที่คุณต้องการ
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}