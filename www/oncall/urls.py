from django.conf.urls import url
from . import views
urlpatterns = [
    # url(r'^reservation/add/((?P<pk>[0-9a-zA-Z]*)/)?$', views.ReservationCreateView.as_view(), name='reservation-create'),
    # url(r'^reservation/view/(?P<pk>[0-9]*)/$', views.ReservationDetailView.as_view(), name='reservation-detail'),
    # url(r'^(?P<status>[0-9a-zA-Z]*)/', views.ReservationListView.as_view(), name='reservation-draft-list'),
    url(r'^$', views.HomeTemplateView.as_view(), name='reservation-list'),
    url(r'^profile/$', views.UserDetailView.as_view(), name='profile-detail'),
]

