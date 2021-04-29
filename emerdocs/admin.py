from django.contrib import admin

from .models import DocPage


class DocPageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'url', 'title', 'title_en')
    empty_value_display = '-пусто-'


admin.site.register(DocPage, DocPageAdmin)
