from django.urls import path, include

from . import views

block_generation = [
    path('proof-of-stake-minting/', views.stake,
         name='proof-of-stake-minting'),
    path('proof-of-work-mining/', views.work, name='proof-of-work-mining'),

]

blockchain_serv = [
    path('introduction-to-emercoin-services/', views.intro_services,
         name='introduction-to-emercoin-services'),
    path('emernvs/', views.emernvs, name='emernvs'),
    path('emerssh/', views.emerssh, name='emerssh'),
    path('emerssl/emerssl-introduction/', views.emerssl_intro,
         name='emerssl-introduction'),
    path('emerssl/emerssl-guide/', views.emerssl_guide, name='emerssl-guide'),
    path('emerssl/emerssl-infocard/', views.emerssl_infocard,
         name='emerssl-infocard'),
    path('emerdns/emerdns-introduction/', views.emerdns_intro,
         name='emerdns-introduction'),
    path('emerdpo/emerdpo-introduction/', views.emerdpo_into,
         name='emerdpo-introduction'),
    path('emerdpo/the-emerdpo-antifake-programme/', views.antifake,
         name='the-emerdpo-antifake-programme'),
    path('emerdpo/emerdpo-sn-publisher', views.sn_publ,
         name='emerdpo-sn-publisher'),
    path('emermagnet/', views.emermagnet, name='emermagnet'),
    path('enumer/', views.enumer, name='enumer'),

]

running_emc = [
    path('linux-quickstart/', views.linux_qs, name='linux-quickstart'),
    path('command-line/', views.command_line, name='command-line'),
    path('emercoin-conf/', views.emercoin_conf, name='emercoin-conf'),
    path('ports/', views.ports, name='ports'),
    path('testnet/', views.testnet, name='testnet'),

]

install_soft = [
    path('core-wallets/gui-wallet/', views.gui_wallet, name='gui-wallet'),
    path('core-wallets/cli-daemon/', views.cli_deamon, name='cli-daemon'),
    path('core-wallets/emerweb-wallet/', views.emerweb, name='emerweb-wallet'),
    path('core-wallets/docker/', views.docker, name='docker'),
    path('other-wallets/', views.other_wallets, name='other-wallets'),
    path('emercert/trusted-diploma/', views.trasted, name='trusted-diploma'),
]

intro = [
    path('the-emc-currency/', views.intro_currency, name='the-emc-currency'),
    path('specifications/', views.specifications, name='specifications'),
    path('security-principles/', views.secutity, name='security-principles'),
]

urlpatterns = [
    path('', views.about_redirect, name='about-redirect'),
    path('about-emercoin/', views.about_emercoin, name='about-emercoin'),
    path('introduction/', include(intro)),
    path('install-software/', include(install_soft)),
    path('running-emercoin/', include(running_emc)),
    path('blockchain-services/', include(blockchain_serv)),
    path('block-generation/', include(block_generation)),
    path('emercoin-api/', views.emer_api, name='emercoin-api'),
    path('emercoin-press-kit/', views.press_kit, name='emercoin-press-kit'),
    path('links-resources/', views.links, name='links-resources')



]
