import os
try:
    from .local_settings import *
except ImportError:
    pass

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGIN_URL = 'login'

SHOP_EMAILS_MANAGERS = ['angara77@gmail.com', 'angara99@gmail.com']
SHOP_EMAIL_FROM = 'angara99@gmail.com'
SHOP_TEL = '+7 (495) 646-99-53'

SHOP_ADDRESS_LINE_1 = 'г.МОСКВА, ул. Соловьиная-Роща 8 к2'
SHOP_ADDRESS_LINE_2 = '1 этаж, офис 9'

SHOP_CONTACT_INFO = {'shop_email': SHOP_EMAIL_FROM, 'shop_tel': SHOP_TEL, 'shop_address': SHOP_ADDRESS_LINE_1 + " " + SHOP_ADDRESS_LINE_2}

SALES_ON_SEARCH = [2274, 2582, 2027] 
SALES_ON_HOME = {'brakes': [2774, 2582, 2560, 2027], 'fuel': [1596, 3160, 1556, 1529], 'body': [2257, 2252, 3508, 3757], 'engine': [3136, 3035, 1932, 1027]}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['dp.loc', 'localhost']



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'dp',
    'products',
    'blogs',
    'home',
    'comments',
    'star_ratings',
    'accounts',
    'admin_photos',
    'email_form',
    'crispy_forms',
    'rest_framework',
    'interlink',
]

SITE_ID = 1

CRISPY_TEMPLATE_PACK = 'bootstrap3'

TAGS_LIST = [
    'задн',
    'передн',
    'лев',
    'прав',
    'внутр',
    'наружн',
    'верхн',
    'нижн',
    'боков',
    'коротк',
    'длинн',
    'всборе',
    'комплект',
    'низ',
    'верх',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dp.urls'



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
                os.path.join(BASE_DIR, 'templates/base')
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'dp.context_processor.small_cart',
                'dp.context_processor.sales_products',
                'dp.context_processor.contact_info',
            ],
        },
    },
]



WSGI_APPLICATION = 'dp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases



DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    'default': {
                'ENGINE': 'django.db.backends.mysql',
                'OPTIONS': { 'read_default_file': os.path.join(BASE_DIR, 'dp/my.cnf'),
                             'sql_mode' : 'traditional',
                    },
        }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

USE_I18N = True
USE_L10N = False
LANGUAGE_CODE = 'ru-RU'
USE_TZ = True
TIME_ZONE = 'Europe/Moscow'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_DIRS = [

    os.path.join(BASE_DIR, "static"),
    local_img_dir,
    
]

STAR_RATINGS_ANONYMOUS = True
STAR_RATINGS_RERATE = False
