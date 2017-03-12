from django import forms
from django.contrib import admin

from . import models
from . import widgets


class ContactPreferenceForm(forms.ModelForm):

    class Meta:
        model = models.ContactPreference
        widgets = {
            'days_of_week': widgets.DaysOfWeekInput(),
        }
        fields = '__all__'


class ContactPreferenceAdmin(admin.ModelAdmin):
  form = ContactPreferenceForm


admin.site.register(models.Rotation)
admin.site.register(models.ContactMethod)
admin.site.register(models.ContactPreference, ContactPreferenceAdmin)
admin.site.register(models.UserProfile)