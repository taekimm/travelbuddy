from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.index, name='loginandres'),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^travels$', views.home, name='home'),
    url(r'^logout$', views.logout),
    url(r'^add$', views.add),
    url(r'^add_plan$', views.add_plan),
    url(r'^destination/(?P<TravelPlanID>\d+)$', views.destination),
    url(r'^join/(?P<TravelPlanID>\d+)$', views.join),
    ]