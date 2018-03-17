from django.db import models


class UrlStorage(models.Model):
    big_url = models.CharField(blank=False, max_length=200)
    count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

