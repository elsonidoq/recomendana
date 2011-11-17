from django.conf.urls.defaults import patterns, include, url

# comment the next two lines to disable the admin:
from django.contrib import admin
from recomendana_prof import models
admin.site.register(models.Account)
admin.site.register(models.Movie)
admin.site.register(models.MovieReview)
admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'recomendana.views.home', name='home'),
    # url(r'^recomendana/', include('recomendana.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
