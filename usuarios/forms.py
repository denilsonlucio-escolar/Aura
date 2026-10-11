from django import forms
from django.contrib.auth.models import User
from .models import Cliente, Endereco

from PIL import Image

class CadastroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    nome = forms.CharField()
    sobrenome = forms.CharField()

    sexo = forms.ChoiceField(
        choices=[('', '---'), ('F', 'Feminino'), ('M', 'Masculino')],
        required=False
    )

    dia = forms.CharField(required=False)
    mes = forms.CharField(required=False)
    ano = forms.CharField(required=False)
    cpf = forms.CharField(required=False)
    telefone = forms.CharField(required=False)

    cep = forms.CharField(required=False)
    estado = forms.CharField(required=False)
    cidade = forms.CharField(required=False)
    bairro = forms.CharField(required=False)
    rua = forms.CharField(required=False)
    numero = forms.CharField(required=False)
    complemento = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class UsuarioForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()

    password = forms.CharField(
        widget=forms.PasswordInput(),
        required=False
    )

    nome = forms.CharField()
    sobrenome = forms.CharField()

    cpf = forms.CharField(required=False)
    telefone = forms.CharField(required=False)
    sexo = forms.CharField(required=False)

    dia = forms.CharField(required=False)
    mes = forms.CharField(required=False)
    ano = forms.CharField(required=False)

    cep = forms.CharField(required=False)
    estado = forms.CharField(required=False)
    cidade = forms.CharField(required=False)
    bairro = forms.CharField(required=False)
    rua = forms.CharField(required=False)
    numero = forms.CharField(required=False)
    complemento = forms.CharField(required=False)