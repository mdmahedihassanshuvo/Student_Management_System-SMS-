# local_settings.py

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sms_dbs',
        'USER': 'postgres',
        'PASSWORD': 'tiger123#',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
