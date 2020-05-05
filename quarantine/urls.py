from django.conf.urls import url
from . import views
# (. significa que importa views da mesma directoria)

urlpatterns = [
    url(r'^$', views.menu, name='menu'),

    url(r'^login/$', views.loginpage, name='loginpage'),
    url(r'^loginview/$', views.loginview, name='loginview'),

    url(r'^registo/$', views.registopage, name='registopage'),
    url(r'^registview/$', views.registview, name='registview'),

    url(r'^logout/$', views.logout_view, name='logout_view'),

    url(r'^criar_grupo/$', views.criargrupopage, name='criargrupopage'),
    url(r'^criargrupo/$', views.criargrupo, name='criargrupo'),

    url(r'^grupo_(?P<grupo_id>[0-9]+)/apagargrupo/$', views.apagargrupo, name='apagargrupo'),


    url(r'^grupo_(?P<grupo_id>[0-9]+)/$', views.grupo_view, name='grupo_view'),
    url(r'^grupo_(?P<grupo_id>[0-9]+)/criarpublicacaopage/$', views.criarpublicacaopage, name='criarpublicacaopage'),
    url(r'^grupo_(?P<grupo_id>[0-9]+)/criarpublicacao/$', views.criarpublicacao, name='criarpublicacao'),
    url(r'^grupo_(?P<grupo_id>[0-9]+)/pub_(?P<pub_id>[0-9]+)/apagarpublicacao/$', views.apagarpublicacao, name='apagarpublicacao'),



    url(r'^grupo_(?P<grupo_id>[0-9]+)/pub_(?P<pub_id>[0-9]+)/$', views.publicacao, name='publicacao'),
    url(r'^grupo_(?P<grupo_id>[0-9]+)/pub_(?P<pub_id>[0-9]+)/publicar/$', views.publicarcomentario,name='publicarcomentario'),
    url(r'^grupo_(?P<grupo_id>[0-9]+)/pub_(?P<pub_id>[0-9]+)/com_(?P<com_id>[0-9]+)/apagarcomentario/$', views.apagarcomentario, name='apagarcomentario'),

    url(r'^grupo_(?P<grupo_id>[0-9]+)/pub_(?P<pub_id>[0-9]+)/votaruppub/$', views.votaruppub, name='votaruppub'),
    url(r'^grupo_(?P<grupo_id>[0-9]+)/pub_(?P<pub_id>[0-9]+)/votardownpub/$', views.votardownpub, name='votardownpub'),


    url(r'^grupo_(?P<grupo_id>[0-9]+)/pub_(?P<pub_id>[0-9]+)/com_(?P<com_id>[0-9]+)/votarupcom/$', views.votarupcom, name='votarupcom'),
    url(r'^grupo_(?P<grupo_id>[0-9]+)/pub_(?P<pub_id>[0-9]+)/com_(?P<com_id>[0-9]+)/votardowncom/$', views.votardowncom, name='votardowncom'),


    #url(r'^grupo_(?P<grupo_id>[0-9]+)/pub_(?P<pub_id>[0-9]+)/com_(?P<com_id>[0-9]+)/votarup/$', views.votarup, name='votarup'),
    #url(r'^grupo_(?P<grupo_id>[0-9]+)/pub_(?P<pub_id>[0-9]+)/com_(?P<com_id>[0-9]+)/votardown/$', views.votardown, name='votardown'),

]