from django.urls import path
from .views import *

urlpatterns = [
    path('', inicial, name='inicial'),
    path('cadastro', cadastro, name='cadastro'),
    path('carrinho', carrinho, name='carrinho'),
    path('login', login, name='login'),
    path('pagamento', pagamento, name='pagamento'),
    path('catalogo', catalogo, name='catalogo'),


    path('add_produtos', add_produtos, name='add_produtos'),
    path('produto/delete/<int:id>/', produto_delete, name='produto_delete'),
    path('produto/editar/<int:id>/', produto_editar, name='produto_editar'),
    path('produtos', produtos, name='produtos'),
]