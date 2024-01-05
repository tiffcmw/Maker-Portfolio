from django.apps import AppConfig

class LoginConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'login'

# defines a subclass of AppConfig, called LoginConfig. 

# AppConfig provides metadata for an application, to specify settings and behaviors for the application.
# Because AppConfig is used in apps.py, it is used as the default configuration.



