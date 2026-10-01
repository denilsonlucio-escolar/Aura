from django.urls import path
from .views import *

urlpatterns = [
    path('', inicial, name='inicial'),

    path('catalogo/', catalogo, name='catalogo'),
    path('carrinho/', carrinho, name='carrinho'),
    path('pagamento/', pagamento, name='pagamento'),
    
    path('carrinho/adicionar/<int:id>/',adicionar_carrinho, name='adicionar_carrinho'),
    path('carrinho/remover/<int:id>/',remover_carrinho, name='remover_carrinho'),
]