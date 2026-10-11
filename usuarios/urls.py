  
from django.urls import path
from .views import *

urlpatterns = [

    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('cadastro/', cadastro, name='cadastro'),

    path('usuarios/', usuarios, name='usuarios'),
    path('usuarios/adicionar/', add_usuario, name='add_usuario'),
    path('usuarios/editar/<int:id>/', usuario_editar, name='usuario_editar'),
    path('usuarios/excluir/<int:id>/', usuario_delete, name='usuario_delete'),

    path('meus_dados/', meus_dados, name='meus_dados'),

    path('painel/', painel, name='painel')
]