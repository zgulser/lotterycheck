
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^playlottery', views.playlottery, name='playlottery'),
    url(r'^confirmation', views.confirmation, name='confirmation'),
    url(r'^playerexists', views.playerexists, name='playerexists'),
    url(r'^winner', views.winner, name='winner'),
]