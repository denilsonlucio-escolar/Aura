from django.contrib import admin
from django.contrib import admin
from .models import Cliente, Endereco, Pagamento, Produto, Pedido, ItemPedido

admin.site.register(Cliente)
admin.site.register(Endereco)
admin.site.register(Pagamento)
admin.site.register(Produto)
admin.site.register(Pedido)
admin.site.register(ItemPedido)
# Register your models here.
