from django.conf.urls import url
from django.contrib.auth import views as auth_views

# . significa que importa views da mesma directoria)
from . import views
from account.views import (
    login_view,
    logout_view,
    registo_view,
    perfilutilizador,
    account_settings
)

urlpatterns = [

    url(r'^$', views.menu, name='menu'),

    # ----------------------------------------------------------------------Account

    url(r'^login/$', login_view, name='login_view'),
    url(r'^registo/$', registo_view, name='registo_view'),
    url(r'^logout/$', logout_view, name='logout_view'),

    # ----------------------------------------------------------------------Utilizador

    url(r'^perfil/(?P<username>[a-zA-Z0-9_]+)/$', perfilutilizador, name='perfilutilizador'),
    url(r'^perfil/(?P<username>[a-zA-Z0-9_]+)/account_settings/$', account_settings, name='account_settings'),

# https://github.com/django/django/blob/master/django/contrib/auth/views.py
    url(r'^perfil/password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
        name='password_change_done'),

    url(r'^perfil/(?P<username>[a-zA-Z0-9_]+)/password_change/', auth_views.PasswordChangeView.as_view(
        template_name='registration/password_change.html'),
        name='password_change'),

    url(r'^password_reset/', auth_views.PasswordResetView.as_view(),
        name='password_reset'),


    url(r'^password_reset/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
        name='password_reset_done'),
    url(r'^reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    url(r'^reset/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
        name='password_reset_complete'),

    # ----------------------------------------------------------------------Grupo

    # url(r'^criar_grupo/$', views.criargrupopage, name='criargrupopage'),
    url(r'^criargrupo/$', views.criargrupo, name='criargrupo'),
    url(r'^grupo_(?P<grupo_id>[0-9]+)/apagargrupo/$', views.apagargrupo, name='apagargrupo'),

    url(r'^grupo_(?P<grupo_id>[0-9]+)/$', views.grupo_view, name='grupo_view'),

    # url(r'^grupo_(?P<grupo_id>[0-9]+)/adicionarmembrospage/$', views.adicionarmembrospage, name='adicionarmembrospage'),
    url(r'^grupo_(?P<grupo_id>[0-9]+)/adicionarmembros/$', views.adicionarmembros, name='adicionarmembros'),

    # url(r'^grupo_(?P<grupo_id>[0-9]+)/removermembrospage/$', views.removermembrospage, name='removermembrospage'),
    url(r'^grupo_(?P<grupo_id>[0-9]+)/removermembros/$', views.removermembros, name='removermembros'),
    url(r'^grupo_(?P<grupo_id>[0-9]+)/sairgrupo/$', views.sairgrupo, name='sairgrupo'),

    # ----------------------------------------------------------------------Publicação

    url(r'^grupo_(?P<grupo_id>[0-9]+)/criarpublicacao/$', views.criarpublicacao, name='criarpublicacao'),
    url(r'^grupo_(?P<grupo_id>[0-9]+)/pub_(?P<pub_id>[0-9]+)/apagarpublicacao/$', views.apagarpublicacao,
        name='apagarpublicacao'),

    url(r'^grupo_(?P<grupo_id>[0-9]+)/pub_(?P<pub_id>[0-9]+)/$', views.publicacao, name='publicacao'),
    url(r'^grupo_(?P<grupo_id>[0-9]+)/pub_(?P<pub_id>[0-9]+)/publicar/$', views.publicarcomentario,
        name='publicarcomentario'),
    url(r'^grupo_(?P<grupo_id>[0-9]+)/pub_(?P<pub_id>[0-9]+)/com_(?P<com_id>[0-9]+)/apagarcomentario/$',
        views.apagarcomentario, name='apagarcomentario'),

    # ----------------------------------------------------------------------Votos

    url(r'^grupo_(?P<grupo_id>[0-9]+)/pub_(?P<pub_id>[0-9]+)/votaruppub/$', views.votaruppub, name='votaruppub'),
    url(r'^grupo_(?P<grupo_id>[0-9]+)/pub_(?P<pub_id>[0-9]+)/votardownpub/$', views.votardownpub, name='votardownpub'),

    url(r'^grupo_(?P<grupo_id>[0-9]+)/pub_(?P<pub_id>[0-9]+)/com_(?P<com_id>[0-9]+)/votarupcom/$', views.votarupcom,
        name='votarupcom'),
    url(r'^grupo_(?P<grupo_id>[0-9]+)/pub_(?P<pub_id>[0-9]+)/com_(?P<com_id>[0-9]+)/votardowncom/$', views.votardowncom,
        name='votardowncom'),

    # url(r'^grupo_(?P<grupo_id>[0-9]+)/pub_(?P<pub_id>[0-9]+)/com_(?P<com_id>[0-9]+)/votarup/$', views.votarup, name='votarup'),
    # url(r'^grupo_(?P<grupo_id>[0-9]+)/pub_(?P<pub_id>[0-9]+)/com_(?P<com_id>[0-9]+)/votardown/$', views.votardown, name='votardown'),

]
