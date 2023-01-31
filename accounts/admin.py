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
        Override get_fieldsets() to add registration_accepted and is_moderator to fieldsets.
        """
        print('')
        print(self.fieldsets)
        print('')
        print(self.fieldsets[2])
        print('')
        print('type(self.fieldsets): ', type(self.fieldsets))

        fieldsets = super().get_fieldsets(request, obj)
        # Try to convert fieldsets to list:
        print('')
        print('type(fieldsets) - tuple: ', type(fieldsets))
        fieldsets = list(fieldsets)
        print('type(fieldsets) - list: ', type(fieldsets))
        print('')
        print(fieldsets)

        # Get the permissions fieldset:
        permissions_fieldset = fieldsets[2]
        print('')
        print('permissions_fieldset: ', permissions_fieldset)
        # Convert permissions_fieldset to list:
        permissions_list = list(permissions_fieldset)
        print('')
        print('permissions_list - list: ', permissions_list)

        # Add `registration_accepted` and `is_moderator` to `permissions_list`:
        permissions_list[1]['fields'] = (
            'is_active',
            'is_staff',
            'is_superuser',
            'registration_accepted',
            'is_moderator',
            'groups',
            'user_permissions',
        )

        # Replace `permissions_fieldset` with updated `permissions_list`:
        fieldsets[2] = tuple(permissions_list)
        
        return fieldsets
