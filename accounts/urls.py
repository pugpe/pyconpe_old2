from django.conf.urls import patterns, url


urlpatterns = patterns('accounts.views',
    url(r'^login/$', 'login'),
    url(r'^profile/$', 'complete_profile'),
)
