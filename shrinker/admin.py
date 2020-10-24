from django.contrib import admin

# Register your models here.
from .models import UrlRedirect


class UrlRedirectAdmin(admin.ModelAdmin):
    list_display = ('user', 'url_original', 'url_new')


admin.site.register(UrlRedirect, UrlRedirectAdmin)
