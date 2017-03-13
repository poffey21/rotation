from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from . import models


class HomeTemplateView(LoginRequiredMixin, generic.TemplateView):
    template_name = '200.html'


class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.UserProfile

    def get_object(self, queryset=None):
        return self.request.user.profile
