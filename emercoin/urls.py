from django.contrib import admin
from django.urls import path, include, re_path

from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


urlpatterns = [
    path(
        'robots.txt',
        TemplateView.as_view(template_name="sitemap/robots.txt",
                             content_type="text/plain"),
    ),
    path(
        'sitemap.xml',
        TemplateView.as_view(template_name='sitemap/sitemap.xml',
                             content_type='application/xml'
                             )
    ),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    # documentation идёт раньше info, иначе catch-all <slug>/ из info.urls
    # перехватит /documentation/
    path('documentation/', include('emerdocs.urls')),
    path('', include('info.urls')),
]

if settings.DEBUG:
    urlpatterns.insert(0, path('admin/', admin.site.urls))
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

handler404 = "info.views.page_not_found"
handler500 = "info.views.server_error"
