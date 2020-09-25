import json
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

with open('config.json') as config_file:
    config = json.load(config_file)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',    
    
    # Allauth
    # 'django.contrib.sites',
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    # 'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.google',

    # REST API
    'rest_framework',
    'rest_framework.authtoken',
    'django_rest_passwordreset',
    # 'corsheaders',

    # Paypal
    'paypal.standard.ipn',

    # Project:
    'api',
    'channels',
    # 'game',
    'game.apps.GameConfig',
    'users',
    'payments',
    'stripe',
    'control',
    # REFERENCE: Djoser authentication: https://www.youtube.com/watch?v=ddB83a4jKSY
    # 'djoser' # Authentication. https://djoser.readthedocs.io/en/latest/index.html 
    # Other
    'import_export',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bingo_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR,'users/templates'),
        ],
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

# AllAuth
#########
# SITE_ID = 1

# LOGIN_REDIRECT_URL = '/'
# SOCIALACCOUNT_QUERY_EMAIL = True

# # Provider specific settings
# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         # For each OAuth based provider, either add a ``SocialApp``
#         # (``socialaccount`` app) containing the required client
#         # credentials, or list them here:
#         'APP': {
#             'client_id': '123',
#             'secret': '456',
#             'key': ''
#         }
#     }
# }

# use custom auth model
USERNAME_FIELD = 'email'

# auth urls
# LOGIN_URL = 'core:login'
# LOGOUT_URL = 'core:logout'
# LOGIN_REDIRECT_URL = 'core:login_redirect'
# LOGOUT_REDIRECT_URL = 'core:home'


# AUTHENTICATION_BACKENDS = [
#     # Needed to login by username in Django admin, regardless of `allauth`
#     'django.contrib.auth.backends.ModelBackend',

#     # `allauth` specific authentication methods, such as login by e-mail
#     'allauth.account.auth_backends.AuthenticationBackend',
# ]

AUTH_USER_MODEL = 'users.User'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication'
        ),
    
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework.permissions.IsAuthenticated',
    #     ),

    # 'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
    # 'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
}


WSGI_APPLICATION = 'bingo_project.wsgi.application'
# Channels
ASGI_APPLICATION = 'bingo_project.routing.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
            # "hosts": [os.environ['REDIS_URL']],
        },
    },
}

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.postgresql_psycopg2',

        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'bingo_db', #LIVE DAATABASE
        'USER': 'bingo_admin',
        'PASSWORD': config['POSTGRES_PASS'],
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Email Setup
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'bingomatrix1@gmail.com'
EMAIL_HOST_PASSWORD = config['EMAIL_HOST_PASSWORD']
DEFAULT_FROM_EMAIL = 'bingomatrix1@gmail.com'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

CURRENCY = config['CURRENCY']
WEBSITE_URL = config['WEBSITE_URL']
NOTIFY_URL = WEBSITE_URL + '/scrambled_URL/'
RETURN_URL = WEBSITE_URL + '/paypal_return/'
CANCEL_URL = WEBSITE_URL + '/paypal_cancel/'

# Billing and Payments
if DEBUG:
    # PayPal
    # Enable PayPal Sandbox - Get it from the account at: https://developer.paypal.com/developer/accounts/
    PAYPAL_RECEIVER_EMAIL = 'bingobulls1-facilitator@gmail.com'  # This is the test BUSINESS account.
    # Buyer account: bingobulls1-buyer@gmail.com / 88776655
    PAYPAL_TEST = True 
    
    # Stripe
    STRIPE_SECRET_KEY = 'sk_test_Ot00cg3oiXBCmssiHmgd1zfz00OoIVzxBV'
    STRIPE_PUBLISHABLE_KEY = 'pk_test_SaQ9IHfske2orxsm3qpyAgnh00V5ILDySH'

else:
    # Paypal
    PAYPAL_RECEIVER_EMAIL = config['PAYPAL_RECEIVER_EMAIL']
    PAYPAL_TEST = False

    # Stripe
    STRIPE_SECRET_KEY = config['STRIPE_SECRET_KEY']
    STRIPE_PUBLISHABLE_KEY = config['STRIPE_PUBLISHABLE_KEY']


IMPORT_EXPORT_USE_TRANSACTIONS = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {"level": "INFO", "handlers": ["file"]},
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "./django.log",
            "formatter": "app",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": True
        },
    },
    "formatters": {
        "app": {
            "format": (
                u"%(asctime)s [%(levelname)-8s] "
                "(%(module)s.%(funcName)s) %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
}