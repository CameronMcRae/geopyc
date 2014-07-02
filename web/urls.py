from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'web.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^control/', include('control.urls', namespace='control')),
    url(r'^admin/', include(admin.site.urls)),
]
