import datetime

from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum

from .forms import ProdutoForm
from usuarios.forms import CadastroForm, UsuarioForm
from produtos.models import Produto
from usuarios.models import Cliente, Endereco


def inicial(request):
    return render(request, 'home.html')


def catalogo(request):
    produtos = Produto.objects.all()
    return render(request, 'catalogo.html', {'produtos': produtos})


def carrinho(request):
    carrinho = request.session.get("carrinho", {})

    produtos = []
    total = 0

    for id, quantidade in carrinho.items():
        produto = Produto.objects.get(pk=id)

        subtotal = produto.preco * quantidade
        total += subtotal

        produtos.append({
            "produto": produto,
            "quantidade": quantidade,
            "subtotal": subtotal
        })

    return render(request, "carrinho.html", {
        "produtos": produtos,
        "total": total
    })


def pagamento(request):
    carrinho = request.session.get("carrinho", {})

    total = 0

    for id, quantidade in carrinho.items():
        produto = get_object_or_404(Produto, pk=id)
        total += produto.preco * quantidade

    context = {
        "total": total,
        "pagina": "pagamento",
    }

    return render(request, "pagamento.html", context)


def adicionar_carrinho(request, id):
    produto = get_object_or_404(Produto, pk=id)

    carrinho = request.session.get("carrinho", {})

    if str(id) in carrinho:
        carrinho[str(id)] += 1
    else:
        carrinho[str(id)] = 1

    request.session["carrinho"] = carrinho

    return redirect("carrinho")

def remover_carrinho(request, id):
    carrinho = request.session.get("carrinho", {})

    if str(id) in carrinho:
        if carrinho[str(id)] > 1:
            carrinho[str(id)] -= 1
        else:
            del carrinho[str(id)]

    request.session["carrinho"] = carrinho

    return redirect("carrinho")

def transparencia(request):
    qtd_produtos = Produto.objects.count()
    
    print("QUANTIDADE DE PRODUTOS:", qtd_produtos)

    context = {
        "qtd_produtos": qtd_produtos,
    }

    return render(request, "transparencia.html", context)
 