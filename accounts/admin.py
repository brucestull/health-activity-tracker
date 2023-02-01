from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from accounts.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = (
        'username',
        'email',
        'registration_accepted',
        'is_moderator',
    )

    def get_fieldsets(self, request, obj=None):
        """
        Override `get_fieldsets()` to add `registration_accepted` and
        `is_moderator` to a `Moderator Permissions` section `CustomUser`
        change view.
        """
        # Get the default `fieldsets` from the superclass `UserAdmin`:
        fieldsets = super().get_fieldsets(request, obj)

        # Convert fieldsets to list:
        fieldsets_as_list = list(fieldsets)

        # Create list of single tuple for `registration_accepted` and `is_moderator`:
        moderator_permissions_as_list = [('Moderator Permissions', {'fields': ('registration_accepted', 'is_moderator')})]
        
        # Combine the two lists and return the result:
        return moderator_permissions_as_list + fieldsets_as_list
