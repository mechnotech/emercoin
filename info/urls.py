from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='emercoin'),
    path('emercoin-blockchain/', views.blockchain, name='blockchain'),
    path('tech-solutions/', views.tech_solutions, name='tech-solutions'),
    path('for-business/', views.for_business, name='for-business'),
    path('for-coinholders/', views.for_coinholders, name='for-coinholders'),
    path('for-developers/', views.for_developers, name='for-developers'),
    path('partners-and-projects/<slug:slug>', views.company, name='partner'),
    path('partners-and-projects/', views.partners, name='partners'),

    ]
