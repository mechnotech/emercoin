from django.urls import path, re_path
from .utils import check_recaptcha
from . import views

urlpatterns = [
    path('', views.index, name='emercoin'),
    re_path(r'^emercoin-blockchain/?$', views.blockchain, name='blockchain'),
    path('emercoin-blockchain/<slug:slug>', views.service, name='service'),
    re_path(r'^tech-solutions/?$',
            views.tech_solutions, name='tech-solutions'),
    re_path(r'^for-business/?$', views.for_business, name='for-business'),
    re_path(r'^for-coinholders/?$',
            views.for_coinholders, name='for-coinholders'),
    re_path(r'^benefits/?$', views.for_coinholders, name='benefits'),
    re_path(r'^for-developers/?$',
            views.for_developers, name='for-developers'),
    re_path(r'^our-social-communities/?$', views.socials, name='socials'),
    path('partners-and-projects/<slug:slug>', views.company, name='partner'),
    re_path(r'^partners-and-projects/?$', views.partners, name='partners'),
    re_path(r'^team/?$', views.team, name='team'),
    path('news/<slug:slug>', views.post, name='post'),
    re_path(r'^news/?$', views.news, name='news'),
    re_path(r'^road-map/?$', views.road_map, name='road-map'),
    re_path(r'^contacts/?$', check_recaptcha(views.contacts), name='contacts'),
    re_path(r'^rate/?$', views.rate, name='rate'),
    path('emercoin-terms-and-conditions', views.terms, name='terms'),
    path('emercoin-privacy-policy', views.privacy, name='privacy'),
    path('<slug:slug>', views.service, name='service'),



    ]
