from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='emercoin'),
    path('emercoin-blockchain/', views.blockchain, name='blockchain'),
    path('tech-solutions/', views.tech_solutions, name='tech-solutions')
    ]