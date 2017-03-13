from django.contrib import admin

from . import models
from . import forms


class RotationMembershipInline(admin.TabularInline):
    model = models.UsersInRotation
    extra = 0


class BundleMembershipInline(admin.TabularInline):
    model = models.RotationsInBundle
    extra = 0


class ContactMethodInline(admin.TabularInline):
    model = models.ContactMethod
    extra = 0


class ContactPreferenceAdmin(admin.ModelAdmin):
    form = forms.ContactPreferenceAdminForm


class UserProfileAdmin(admin.ModelAdmin):
    inlines = (ContactMethodInline,)


class RotationAdmin(admin.ModelAdmin):
    form = forms.RotationAdminForm
    inlines = (RotationMembershipInline, )


class BundleAdmin(admin.ModelAdmin):
    inlines = (BundleMembershipInline, )


admin.site.register(models.Rotation, RotationAdmin)
admin.site.register(models.ContactPreference, ContactPreferenceAdmin)
admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.Bundle, BundleAdmin)
