from django.conf.urls import patterns, include, url

urlpatterns = patterns('tables.views',
	url(r'^ri/accounts=(.*)/$', 'GetRI'),
	url(r'^ri/showtable/$', 'ShowTable'),
)
