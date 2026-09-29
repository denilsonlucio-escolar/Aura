from django import forms
from django.contrib.auth.models import User
from .models import Produto

from PIL import Image


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco', 'estoque', 'imagem']

    def clean_imagem(self):
        imagem = self.cleaned_data.get('imagem')

        if imagem:
            extensoes_permitidas = ['.jpg', '.jpeg', '.png', '.webp']
            nome = imagem.name.lower()

            if not any(nome.endswith(ext) for ext in extensoes_permitidas):
                raise forms.ValidationError('Formato não permitido. Use JPG, PNG ou WEBP.')

            limite_mb = 2
            if imagem.size > limite_mb * 1024 * 1024:
                raise forms.ValidationError(f'A imagem deve ter no máximo {limite_mb}MB.')

            try:
                largura, altura = Image.open(imagem).size
            except Exception:
                raise forms.ValidationError('Não foi possível processar essa imagem.')

            imagem.seek(0)

            if largura < 400 or altura < 400:
                raise forms.ValidationError('A imagem deve ter no mínimo 400x400 pixels.')

        return imagem
