from django.contrib import admin
from .models import Promo


class PromoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'link', 'bg_color', 'mobile_img', 'desktop_img')


admin.site.register(Promo, PromoAdmin)
