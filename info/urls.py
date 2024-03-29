from django.urls import path, re_path
from .utils import check_recaptcha
from . import views
from emerdocs import views as doc_views
from .feeds import MyFeed

urlpatterns = [
    path('', views.index, name='emercoin'),
    # Хардкодим старые URL`s

    path('2015-01-15-Emercoin_Reaches_Peering_Agreement_with_OpenNIC',
         views.url1, name='url1'),
    path('emcdpo-zh', doc_views.url1),
    path('DNS_and_Name-Value_Storage', doc_views.url2),
    path('EMCDNS_and_NVS', doc_views.url2),
    path('feed', MyFeed(), name='news_feed'),
    path('feeds', MyFeed()),
    path('rss', MyFeed(), name='news_feed'),
    # ------------------------
    path('emercoin-blockchain/<slug:slug>', views.service, name='service'),
    re_path(r'^emercoin-blockchain/?$', views.blockchain, name='blockchain'),
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
    path('news/<slug:slug>/', views.post, name='post'),
    re_path(r'^news/?$', views.news, name='news'),
    re_path(r'^road-map/?$', views.road_map, name='road-map'),
    re_path(r'^contacts/?$', check_recaptcha(views.contacts), name='contacts'),
    re_path(r'^rate/?$', views.rate, name='rate'),
    path('emercoin-terms-and-conditions', views.terms, name='terms'),
    path('emercoin-privacy-policy', views.privacy, name='privacy'),
    re_path(r'^getstarted/?$', views.for_developers, name='getstarted'),
    path('<slug:slug>/', views.service, name='service'),

]
