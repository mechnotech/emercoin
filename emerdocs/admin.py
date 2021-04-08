from django.contrib import admin

from .models import DocPage


class DocPageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'url',)
    empty_value_display = '-пусто-'


admin.site.register(DocPage, DocPageAdmin)
