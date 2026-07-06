from django import forms
from .models import Cliente, Endereco, Pagamento, Produto, Pedido, ItemPedido

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco', 'estoque', 'imagem']