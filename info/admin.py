from django.contrib import admin
from .models import Promo, AboutEmer, Services


class PromoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'link', 'bg_color', 'mobile_img', 'desktop_img')


class AboutEmerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'image')


class ServicesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'scenarios', 'image')


admin.site.register(Promo, PromoAdmin)
admin.site.register(AboutEmer, AboutEmerAdmin)
admin.site.register(Services, ServicesAdmin)
