from django import forms

from . import models
from . import widgets


class ContactPreferenceAdminForm(forms.ModelForm):

    class Meta:
        model = models.ContactPreference
        widgets = {
            'days_of_week': widgets.DaysOfWeekInput(),
        }
        fields = '__all__'


class RotationAdminForm(forms.ModelForm):

    class Meta:
        model = models.Rotation
        widgets = {
            'days_of_week': widgets.DaysOfWeekInput(),
        }
        fields = '__all__'
