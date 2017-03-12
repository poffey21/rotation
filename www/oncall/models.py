from __future__ import unicode_literals

from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.core.validators import validate_comma_separated_integer_list
from django.db import models
from django.db.models import Q


class Duty(models.Model):
    days_of_week = models.CharField(max_length=16, validators=[validate_comma_separated_integer_list])
    start_time = models.IntegerField(help_text='Hour in the Day')
    stop_time = models.IntegerField(help_text='Hour in the Day')

    def validate_unique(self, *args, **kwargs):
        super(Duty, self).validate_unique(*args, **kwargs)
        q_objects = Q()
        for day in self.days_of_week.split(','):
            q_objects.add(Q(days_of_week__contains=day), Q.OR)

        qs = kwargs.get('qs', self.__class__._default_manager.filter(q_objects))

        if not self._state.adding and self.pk is not None:
            qs = qs.exclude(pk=self.pk)

        for obj in qs:
            x = range(self.start_time, self.stop_time)
            y = range(obj.start_time, obj.stop_time)
            if set(x).intersection(y):
                raise ValidationError({
                    NON_FIELD_ERRORS: ['You have an overlapping date range.', ],
                })

    class Meta:
        abstract = True


class UserProfile(models.Model):
    """
    Default User Profile that ties extra attributes to user
    """

    user = models.OneToOneField('auth.User', related_name='profile')
    notify = models.BooleanField(help_text='Notify when on-call')


class ContactMethod(models.Model):
    CONTACT_METHOD_OPTIONS = (
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('text', 'text'),
        ('webhook', 'Webhook'),
    )
    user = models.ForeignKey('auth.User')
    method = models.CharField('Email/Phone/Text', choices=CONTACT_METHOD_OPTIONS, max_length=16)
    details = models.CharField(max_length=64)


class ContactPreference(Duty):
    user = models.ForeignKey('auth.User')
    contact_method = models.ForeignKey('oncall.ContactMethod')

    def validate_unique(self, *args, **kwargs):
        # TODO: filter only a ingle user schedules
        super(Duty, self).validate_unique(*args, **kwargs)

class UsersInRotation(models.Model):
    user = models.ForeignKey('auth.User')
    rotation = models.ForeignKey('oncall.Rotation')
    order = models.IntegerField('Order in the rotation')


class Rotation(Duty):
    """
    The on-call rotations available
    """
    group = models.ForeignKey('auth.Group')
    length = models.IntegerField('Length of rotation. Set to zero if primary is always set.')
    users = models.ManyToManyField('auth.User', through='oncall.UsersInRotation')
    order = models.IntegerField('Priority')

    def validate_unique(self, *args, **kwargs):
        # TODO: filter only a group's schedules
        super(Duty, self).validate_unique(*args, **kwargs)

