from django.conf.urls import patterns, url
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('core.views',
    url(r'^$', direct_to_template, {'template': 'index.html'}, name='index'),

)
