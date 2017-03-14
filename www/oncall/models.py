from __future__ import unicode_literals

from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.core.validators import validate_comma_separated_integer_list
from django.db import models
from django.db.models import Q


class Duty(models.Model):
    HOURS_IN_THE_DAY = [
        [x % 12 + 12 * i, '%s%s' % (x, y)]
        for i, y in enumerate(['am', 'pm'])
        for x in [12] + range(1, 12)
    ] + [[24, '12am (next day)']]

    order_attribute = None

    days_of_week = models.CharField(max_length=16, validators=[validate_comma_separated_integer_list])
    start_time = models.IntegerField(help_text='Hour in the Day', choices=HOURS_IN_THE_DAY)
    stop_time = models.IntegerField(help_text='Hour in the Day', choices=HOURS_IN_THE_DAY)

    def validate_unique(self, *args, **kwargs):
        initial_qs = kwargs.pop('qs') or self.__class__._default_manager.all()
        super(Duty, self).validate_unique(*args, **kwargs)

        if self.start_time == self.stop_time:
            raise ValidationError({
                NON_FIELD_ERRORS: ['Start time and Stop time cannot be the same.', ],
            })

        q_objects = Q()
        for day in self.days_of_week.split(','):
            q_objects.add(Q(days_of_week__contains=day), Q.OR)

        qs = initial_qs.filter(q_objects)
        if not self._state.adding and self.pk is not None:
            qs = qs.exclude(pk=self.pk)

        for obj in qs:
            next_day_for_x, next_day_for_y = 0, 0
            if self.start_time > self.stop_time:
                next_day_for_x = 12
            if obj.start_time > obj.stop_time:
                next_day_for_y = 12
            x = range(self.start_time, self.stop_time + next_day_for_x)
            y = range(obj.start_time, obj.stop_time + next_day_for_y)
            if set(x).intersection(y):
                raise ValidationError({
                    NON_FIELD_ERRORS: ['You have an overlapping date range.', ],
                })

        # #####################################
        # # Search for next day conflicts now #
        # #####################################
        # q_objects = Q()
        # for day in self.days_of_week.split(','):
        #     q_objects.add(Q(days_of_week__contains=day), Q.OR)
        #
        # qs = initial_qs.filter(q_objects)
        # if not self._state.adding and self.pk is not None:
        #     qs = qs.exclude(pk=self.pk)
        #
        # for obj in qs:
        #     next_day_for_x, next_day_for_y = 0, 0
        #     if self.start_time > self.stop_time:
        #         next_day_for_x = 12
        #     if obj.start_time > obj.stop_time:
        #         next_day_for_y = 12
        #     x = range(self.start_time, self.stop_time + next_day_for_x)
        #     y = range(obj.start_time, obj.stop_time + next_day_for_y)
        #     if set(x).intersection(y):
        #         raise ValidationError({
        #             NON_FIELD_ERRORS: ['You have an overlapping date range.', ],
        #         })

    def get_days_of_week_display(self):
        DAYS_OF_WEEK = ['M', 'T', 'W', 'Th', 'F', 'S', 'Su']
        return ', '.join([DAYS_OF_WEEK[int(x)] for x in self.days_of_week.split(',')])

    class Meta:
        abstract = True


class UserProfile(models.Model):
    """
    Default User Profile that ties extra attributes to user
    """

    user = models.OneToOneField('auth.User', related_name='profile')
    notify = models.BooleanField(help_text='Notify when on-call', default=False)

    def __str__(self):
        return self.user.__str__()

    def __unicode__(self):
        return self.__str__()


class ContactMethod(models.Model):
    CONTACT_METHOD_OPTIONS = (
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('text', 'Text Message'),
        ('webhook', 'Webhook'),
    )
    user_profile = models.ForeignKey('oncall.UserProfile')
    method = models.CharField('Email/Phone/Text', choices=CONTACT_METHOD_OPTIONS, max_length=16)
    details = models.CharField(max_length=64)

    def __str__(self):
        return '{}: {}'.format(self.get_method_display(), self.details)

    def __unicode__(self):
        return self.__str__()


class ContactPreference(Duty):
    user = models.ForeignKey('auth.User')
    contact_method = models.ForeignKey('oncall.ContactMethod')

    def validate_unique(self, *args, **kwargs):
        qs = self.__class__._default_manager.filter(user=self.user)
        super(ContactPreference, self).validate_unique(qs=qs, *args, **kwargs)

    def __str__(self):
        return self.user.__str__()

    def __unicode__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Contact Schedule'
        verbose_name_plural = 'Contact Schedules'


class UsersInRotation(models.Model):
    user = models.ForeignKey('auth.User')
    rotation = models.ForeignKey('oncall.Rotation')
    order = models.IntegerField('Order in the rotation')


class Rotation(Duty):
    """
    The on-call rotations available
    """
    group = models.ForeignKey('auth.Group')
    length = models.IntegerField('Users to be contacted before escalation. Set to zero if primary is always set.')
    users = models.ManyToManyField('auth.User', through='oncall.UsersInRotation')

    def validate_unique(self, *args, **kwargs):
        qs = self.__class__._default_manager.filter(group=self.group)
        super(Duty, self).validate_unique(qs=qs, *args, **kwargs)

    def __str__(self):
        return '{}: {} | {}-{}'.format(
            self.group.__str__(), self.get_days_of_week_display().__str__(),
            self.get_start_time_display(), self.get_stop_time_display(),
        )

    def __unicode__(self):
        return self.__str__()


class RotationsInBundle(models.Model):
    SUPPORT_LEVELS = (
        ('1', 'Tier 2'),
        ('2', 'Tier 3'),
        ('3', 'Management'),
    )
    bundle = models.ForeignKey('oncall.Bundle')
    rotation = models.ForeignKey('oncall.Rotation')
    order = models.IntegerField('Order in the rotation', choices=SUPPORT_LEVELS)


class Bundle(models.Model):
    """ A bundle of Configuration Items that need an on-call rotation"""
    name = models.CharField(max_length=64)
    external_id = models.CharField(max_length=32, blank=True)
    rotations = models.ManyToManyField('oncall.Rotation', through='oncall.RotationsInBundle')

    class Meta:
        verbose_name = 'Support Bundle'
        verbose_name_plural = 'Support Bundles'