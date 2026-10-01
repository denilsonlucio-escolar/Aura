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

