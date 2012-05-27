from django.conf.urls import patterns, url

urlpatterns = patterns('core.views',
    url(r'^$',
        view='index',
        name='index',
    ),
)
