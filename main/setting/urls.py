"""setting URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^$', view=TemplateView.as_view(template_name="index.html"), name='index_view'),
    url(r'^anniversary/$', view=TemplateView.as_view(template_name="abc.html"), name='anni_view'),
    url(r'^url_shrt/', include('urlshorter.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^google0b068d3c0cad51d3.html$', TemplateView.as_view(template_name='google0b068d3c0cad51d3.html', content_type='text/plain')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

