from django.contrib import admin
from .models import UrlStorage

class URLAdmin(admin.ModelAdmin):
    search_fields = ('big_url',)
    list_display = ('id', 'big_url', 'count','created_at')



admin.site.register(UrlStorage,URLAdmin)