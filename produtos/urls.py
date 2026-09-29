from django.urls import path
from .views import *

urlpatterns = [
    path('produtos/', produtos, name='produtos'),
    path('produtos/adicionar/', add_produtos, name='add_produtos'),
    path('produtos/editar/<int:id>/', produto_editar, name='produto_editar'),
    path('produtos/excluir/<int:id>/', produto_delete, name='produto_delete'),
    path('produtos/<int:id>/', produto_detalhe, name='produto_detalhe'),
]