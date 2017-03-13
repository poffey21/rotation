from django.contrib import admin

from . import models
from . import forms


class ContactPreferenceAdmin(admin.ModelAdmin):
  form = forms.ContactPreferenceAdminForm



class RotationAdmin(admin.ModelAdmin):
  form = forms.RotationAdminForm


admin.site.register(models.Rotation, RotationAdmin)
admin.site.register(models.ContactMethod)
admin.site.register(models.ContactPreference, ContactPreferenceAdmin)
admin.site.register(models.UserProfile)