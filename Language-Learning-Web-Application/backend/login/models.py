from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

# Models provide information about the data, and also store the data
# each class is a table in the database configured in settings.py
# each table in the database has a unique identifier called a primary key, specified by primary_key=True
# I used a google cloud hosted postgresql database, and i used a proxy to connect to it locally. 
# updating these fields require 
# python manage.py makemigrations
# python manage.py migrate
# for them to be configured correctly
# these tables are imported in views to be accessed

# these can also be configured in other ways such as using psql command line or pgadmin
# however it HAS to be made sure that all the tables are match correctly orelse there will be problems with the views
# i created these really early on, but i don't need i now that i'm using django existing auth method. 
# i thought to create it solely for the auth_type, but since i won't be implementing google auth in a while
# due to the many requirements it needs, i probably will migrate to this database later in the development stage
# its just me, a singular localhost user on the default django auth user table anyways.

# Users
class User(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True, null=False)
    email = models.EmailField(max_length=255, unique=True, null=False)
    password = models.CharField(max_length=255)  # Changed from password_hash
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # New field
    
    # I have not implemented google login yet since it requires a public website and legal docs
    AUTH_TYPES = [
        ('local', 'Local'),
        ('google', 'Google'),
        # Add more auth types if necessary, for now I just have local. 
    ]
    
    auth_type = models.CharField(max_length=50, choices=AUTH_TYPES, default='local')
    date_created = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)  # Changed to auto_now
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()  # Added custom manager

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    
    class Meta:
        db_table = 'User'  # Use the exact table name

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        if self.model.objects.filter(email=email).exists():
            raise ValueError('A user with this email already exists')
        if self.model.objects.filter(username=username).exists():
            raise ValueError('A user with this username already exists')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user