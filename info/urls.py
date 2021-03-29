from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='emercoin'),
    path('emercoin-blockchain/', views.blockchain, name='blockchain'),
    path('emercoin-blockchain/<slug:slug>', views.service, name='service'),
    path('tech-solutions/', views.tech_solutions, name='tech-solutions'),
    path('for-business/', views.for_business, name='for-business'),
    path('for-coinholders/', views.for_coinholders, name='for-coinholders'),
    path('benefits/', views.for_coinholders, name='benefits'),
    path('for-developers/', views.for_developers, name='for-developers'),
    path('our-social-communities/', views.socials, name='socials'),
    path('partners-and-projects/<slug:slug>', views.company, name='partner'),
    path('partners-and-projects/', views.partners, name='partners'),


    ]
