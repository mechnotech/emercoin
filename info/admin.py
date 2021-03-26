from django.contrib import admin
from .models import (
    Promo, AboutEmer, Services, Media, RoadMap, Content, News, Person
)


class PromoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'link', 'bg_color', 'mobile_img', 'desktop_img')
    empty_value_display = '-пусто-'


class AboutEmerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'image')
    empty_value_display = '-пусто-'


class ServicesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'scenarios', 'image')
    empty_value_display = '-пусто-'


class ContentInline(admin.TabularInline):
    model = Media.contents.through
    extra = 1
    verbose_name = 'контент'


class MediaAdmin(admin.ModelAdmin):
    inlines = (ContentInline,)
    list_display = ('pk', 'name', 'logo')
    empty_value_display = '-пусто-'


class ContentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'date', 'brif', 'link')
    empty_value_display = '-пусто-'


class RoadMapAdmin(admin.ModelAdmin):
    list_display = ('pk', 'year', 'text')
    empty_value_display = '-пусто-'


class NewsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'date', 'title', 'slug', 'image', 'text')
    empty_value_display = '-пусто-'


class PersonAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'whois', 'is_team', 'is_adviser')
    empty_value_display = '-пусто-'


admin.site.register(Promo, PromoAdmin)
admin.site.register(AboutEmer, AboutEmerAdmin)
admin.site.register(Services, ServicesAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(Content, ContentAdmin)
admin.site.register(RoadMap, RoadMapAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Person, PersonAdmin)
