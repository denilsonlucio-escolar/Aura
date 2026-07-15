from django.urls import path
from .views import *

urlpatterns = [
    path('', inicial, name='inicial'),

    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('cadastro/', cadastro, name='cadastro'),

    path('catalogo/', catalogo, name='catalogo'),
    path('produto/<int:id>/', produto_detalhe, name='produto_detalhe'),
    path('carrinho/', carrinho, name='carrinho'),
    path('pagamento/', pagamento, name='pagamento'),

    path('produtos/', produtos, name='produtos'),
    path('produtos/adicionar/', add_produtos, name='add_produtos'),
    path('produtos/editar/<int:id>/', produto_editar, name='produto_editar'),
    path('produtos/excluir/<int:id>/', produto_delete, name='produto_delete'),

    path('meus_dados/', meus_dados, name='meus_dados'),

    path('usuarios/', usuarios, name='usuarios'),
    path('usuarios/adicionar/', add_usuario, name='add_usuario'),
    path('usuarios/editar/<int:id>/', usuario_editar, name='usuario_editar'),
    path('usuarios/excluir/<int:id>/', usuario_delete, name='usuario_delete'),

    path('painel/', painel, name='painel')
]