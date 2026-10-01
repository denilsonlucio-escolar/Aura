from django.db import models

from django.db import models
from django.contrib.auth.models import User

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
