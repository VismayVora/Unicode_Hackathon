from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import User,Vendor

# Register your models here.
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ['email', 'name','is_client','is_vendor','is_staff','is_active','is_superuser']
    list_filter = ['email','name','is_client','is_vendor','is_staff','is_active','is_superuser']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name',),}),
        ('Permissions', {'fields': ('is_active','is_staff','is_client','is_vendor','is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide,'),
            'fields': ('email', 'password1', 'password2', 'name','is_staff','is_active','is_client','is_vendor'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

class VendorAdmin(BaseUserAdmin):
    model = Vendor
    list_display = ['email', 'name','phone_no','is_client','is_vendor','is_staff','is_active','is_superuser','industry_category']
    list_filter = ['email','name','phone_no','is_client','is_vendor','is_staff','is_active','is_superuser','industry_category']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name','phone_no','industry_category'),}),
        ('Permissions', {'fields': ('is_active','is_staff','is_client','is_vendor','is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide,'),
            'fields': ('email','phone_no', 'password1', 'password2', 'name','is_staff','is_active','is_client','is_vendor','industry_category'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.register(Vendor, VendorAdmin)