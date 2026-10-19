from django.db import models

from usuarios.models import Cliente
from produtos.models import Produto

class Pedido(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="pedidos"  
    )

#   pagamento = models.ForeignKey(
#       Pagamento,
#       on_delete=models.SET_NULL,
#       null=True,
#       blank=True,
#       related_name="pedidos"
#   )

    data_pedido = models.DateTimeField("Data do Pedido", auto_now_add=True)
    status = models.CharField("Status", max_length=45)

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.nome}"


class ItemPedido(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name="itens"
    )

    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name="itens"
    )

    quantidade = models.IntegerField("Quantidade")
    preco_unitario = models.DecimalField(
        "Preço Unitário",
        max_digits=10,
        decimal_places=2
    )

    def subtotal(self):
        return self.quantidade * self.preco_unitario

    def __str__(self):
        return f"{self.produto.nome} x {self.quantidade}"