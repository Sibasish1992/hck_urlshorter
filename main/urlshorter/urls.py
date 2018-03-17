from django.conf.urls import url, include
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    url(r'^$',view=csrf_exempt(views.HomeView.as_view()), name='short_url_index'),
    url(r'^clean-urls/$', view=csrf_exempt(views.CleanUrlView.as_view()), name='clean_url'),
    url(r'^fetch/short-url/$', view=csrf_exempt(views.ShortURLView.as_view()), name='short_url'),
    url(r'^fetch/long-url/$', view=csrf_exempt(views.LongURLView.as_view()), name='long_url'),
    url(r'^fetch/short-urls/$',view=csrf_exempt(views.ShortURLSView.as_view()), name='short_urls'),
    url(r'^fetch/count/$',view=csrf_exempt(views.HitCountView.as_view()), name='count_hits'),
    url(r'^fetch/long-urls/$',view=csrf_exempt(views.LongURLSView.as_view()), name='long_urls'),
    url(r'^(?P<short_url_hash>[\w-]+)/$', view=csrf_exempt(views.RedirectToView.as_view()), name='haser_redirect'),
]