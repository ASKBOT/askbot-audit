"""
askbot audit url configuraion file
"""
try:
    from django.conf.urls import url, patterns, include
    from django.conf.urls import handler404
except ImportError:
    from django.conf.urls.defaults import url, patterns, include
    from django.conf.urls.defaults import handler404

from . import views

urlpatterns = patterns('',
    url('$', views.home, name='audit_home'),
    url('load-items/$', views.LoadItems().as_view(), name='audit_load_items')
)
