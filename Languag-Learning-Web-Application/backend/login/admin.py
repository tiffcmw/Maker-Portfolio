from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

# Custom forms for User creation
# Inherits from UserCreationForm

# the traditional user creation form doesn't have the auth_type field,
# so I have to create a custom form to include it

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password', 'auth_type')
        

class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('username', 'email', 'password', 'auth_type')

# Admin interface for User model
class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('user_id', 'username', 'email', 'auth_type', 'is_superuser', 'is_staff', 'date_created', 'last_updated')
    list_filter = ('auth_type', 'is_superuser', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'auth_type')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff')}),
        ('Important dates', {'fields': ('date_created', 'last_updated')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'auth_type'),
        }),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)
    filter_horizontal = ()

# Register the User model with the admin site
admin.site.register(User, UserAdmin)