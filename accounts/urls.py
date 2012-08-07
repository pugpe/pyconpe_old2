from django.conf.urls import patterns, url


urlpatterns = patterns('accounts.views',
    url(r'^register/$', 'register'),
    url(r'^profile/$', 'complete_profile'),
)
