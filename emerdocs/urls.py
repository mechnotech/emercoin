from django.urls import path

from . import views

urlpatterns = [
    path('', views.about_redirect, name='about-redirect'),
    path('about-emercoin/', views.about_emercoin, name='about-emercoin'),
    path('introduction/the-emc-currency', views.intro_currency,
         name='the-emc-currency'),
    path('introduction/specifications', views.specifications,
         name='specifications'),

    ]