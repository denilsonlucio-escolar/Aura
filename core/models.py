from django.db import models

from django.db import models
from django.contrib.auth.models import User
from usuarios.models import Cliente


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


