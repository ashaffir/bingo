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
DEBUG = True if config['DEBUG'] == 'True' else False


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
    'django.contrib.sitemaps',

    # Allauth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',

    # REST API
    'rest_framework',
    'rest_framework.authtoken',
    'django_rest_passwordreset',
    'corsheaders',
    'django_extensions',

    # Paypal
    'paypal.standard.ipn',

    # Project:
    'api',
    'channels',
    # 'game',
    'bingo_main',
    'game.apps.GameConfig',
    'users',
    'payments',
    'stripe',
    'control',
    'administration',
    'frontend',
    # REFERENCE: Djoser authentication: https://www.youtube.com/watch?v=ddB83a4jKSY
    # 'djoser' # Authentication. https://djoser.readthedocs.io/en/latest/index.html
    # Other
    'import_export',
    'ckeditor',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bingo_project.urls'

TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            TEMPLATE_DIR,
            os.path.join(BASE_DIR, 'users/templates'),
            os.path.join(BASE_DIR, 'bingo_main/templates'),
            os.path.join(BASE_DIR, 'frontend/templates'),
            os.path.join(BASE_DIR, 'administration/templates'),
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
SITE_ID = 1
ACCOUNT_EMAIL_REQUIRED = True
LOGIN_REDIRECT_URL = '/'


AUTH_USER_MODEL = 'users.User'
USERNAME_FIELD = 'email'

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
SOCIALACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': [
            'email',
            ],
    },
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

# SOCIALACCOUNT_QUERY_EMAIL = True

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
# USERNAME_FIELD = 'email'

# auth urls
# LOGIN_URL = 'core:login'
# LOGOUT_URL = 'core:logout'
# LOGIN_REDIRECT_URL = 'core:login_redirect'
# LOGOUT_REDIRECT_URL = 'core:home'


AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

# AUTH_USER_MODEL = 'users.User'


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
        'NAME': 'bingo_db',  # LIVE DAATABASE
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

LANGUAGES = [
    ('en', 'English'),
    ('he', 'Hebrew'),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

# Zoho email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'support@polybingo.com'
EMAIL_HOST_PASSWORD = config['EMAIL_HOST_PASSWORD_ZOHO']
DEFAULT_FROM_EMAIL = 'Polybingo<support@polybingo.com>'


# Gmail Email Setup
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_USE_TLS = True
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'polybingocom@gmail.com'
# EMAIL_HOST_PASSWORD = config['EMAIL_HOST_PASSWORD']
# DEFAULT_FROM_EMAIL = 'polybingocom@gmail.com'

ADMIN_EMAIL = config['ADMIN_EMAIL']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DATA_UPLOAD_MAX_MEMORY_SIZE = config['DATA_UPLOAD_MAX_MEMORY_SIZE']

CURRENCY = config['CURRENCY']
WEBSITE_URL = config['WEBSITE_URL']
NOTIFY_URL = WEBSITE_URL + '/scrambled_URL/'
RETURN_URL = WEBSITE_URL + '/paypal_return/'
CANCEL_URL = WEBSITE_URL + '/paypal_cancel/'

# Billing and Payments
if DEBUG:
    # PayPal
    # Enable PayPal Sandbox - Get it from the account at: https://developer.paypal.com/developer/accounts/
    # This is the test BUSINESS account.
    PAYPAL_RECEIVER_EMAIL = 'sb-gtvz474007739@business.example.com'
    PAYPAL_TEST = True

    # Stripe
    STRIPE_SECRET_KEY = 'sk_test_51Hl7auEkukXQn9UkO81pPliqX4W2cn8DgtKQ27qYdGZtGtVZYXycppw92O00KwksWM5NRdqfcD10AxK6ETkxeyeb00fjwmKLGq'
    STRIPE_PUBLISHABLE_KEY = 'pk_test_51Hl7auEkukXQn9Uks2cDolcq8H2GgjWhii5tdCRGhvXXS35hgOJJAtA9ij1TfVOdwy2ngP8zMnsat1SZMPYb20Zu00SAqw4E4C'

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
