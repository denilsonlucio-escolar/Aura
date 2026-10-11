from django.db import models
from django.contrib.auth.models import User
from usuarios.models import Cliente


class Pagamento(models.Model):
    forma_pagamento = models.CharField("Forma de Pagamento", max_length=45)
    status = models.CharField("Status", max_length=45)

    def __str__(self):
        return self.forma_pagamento