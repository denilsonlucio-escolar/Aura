from django.db import models


from django.db import models
from django.contrib.auth.models import User


class Cliente(models.Model):
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="cliente",
        null=True,
        blank=True
    )

    nome = models.CharField("Nome", max_length=120)
    sobrenome = models.CharField("Sobrenome", max_length=120, blank=True, default="")
    email = models.EmailField("E-mail", unique=True)
    senha = models.CharField("Senha", max_length=128)
    telefone = models.CharField("Telefone", max_length=20, blank=True, default="")

    sexo = models.CharField("Sexo", max_length=1, blank=True, default="")
    data_nascimento = models.DateField("Data de Nascimento", null=True, blank=True)
    cpf = models.CharField("CPF", max_length=14, blank=True, default="")

    def __str__(self):
        return self.nome


class Endereco(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="enderecos"
    )
    rua = models.CharField("Rua", max_length=45)
    numero = models.CharField("Número", max_length=10, blank=True, default="")
    complemento = models.CharField("Complemento", max_length=60, blank=True, default="")
    bairro = models.CharField("Bairro", max_length=60, blank=True, default="")
    cidade = models.CharField("Cidade", max_length=45)
    estado = models.CharField("Estado", max_length=45)
    cep = models.CharField("CEP", max_length=20)

    def __str__(self):
        return f"{self.rua} - {self.cidade}"


class Pagamento(models.Model):
    forma_pagamento = models.CharField("Forma de Pagamento", max_length=45)
    status = models.CharField("Status", max_length=45)

    def __str__(self):
        return self.forma_pagamento


class Produto(models.Model):
    nome = models.CharField("Nome", max_length=120)
    descricao = models.TextField("Descrição")
    preco = models.DecimalField("Preço", max_digits=10, decimal_places=2)
    estoque = models.IntegerField("Estoque")

    imagem = models.ImageField(
        "Imagem",
        upload_to="produtos/",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.nome


class Pedido(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="pedidos"
    )

    pagamento = models.ForeignKey(
        Pagamento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pedidos"
    )

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