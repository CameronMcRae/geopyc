from django.conf.urls import patterns, include, url
from django.contrib import admin
from control import views

urlpatterns = patterns('',
    url(r'^results/', views.results, name='results'),
    url(r'^analysis/', views.analysis, name='analysis'),
    url(r'^run/(?P<method_id>\d+)/$', views.run, name='run'),
    url(r'^$', include(admin.site.urls)),
    url(r'^methods/', include(admin.site.urls)),
    url(r'^detail/(?P<method_id>\d+)/$', views.detail, name='detail'),
    url(r'^index/', views.index, name='index'),
    url(r'^history/', views.run_history, name='history'),
)
