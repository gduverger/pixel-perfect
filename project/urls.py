from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

from project import settings

import app.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', app.views.index, name='index'),
    url(r'^upload/?$', app.views.upload, name='upload'),
    url(r'^admin/', include(admin.site.urls)),

)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
