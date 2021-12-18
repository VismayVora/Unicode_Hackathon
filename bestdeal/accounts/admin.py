from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User

# Register your models here.
class UserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'pincode', 'phone','is_staff','is_active']
    list_filter = ['email', 'pincode', 'phone','is_staff','is_active']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('pincode','phone')}),
        ('Permissions', {'fields': ('is_active','is_staff')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide,'),
            'fields': ('email', 'password1', 'password2', 'phone', 'pincode','is_staff','is_active'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)