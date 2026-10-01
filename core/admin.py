from django.contrib import admin
from django.contrib import admin
from .models import Pagamento, Produto, Pedido, ItemPedido
from .models import Pagamento, Produto, Pedido, ItemPedido
from usuarios.models import Cliente, Endereco

admin.site.register(Cliente)
admin.site.register(Endereco)
admin.site.register(Pagamento)
admin.site.register(Produto)
admin.site.register(Pedido)
admin.site.register(ItemPedido)
# Register your models here.
