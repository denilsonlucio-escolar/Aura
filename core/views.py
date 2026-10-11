from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Min, Max
from produtos.models import Produto, Categoria
from pedidos.models import Pedido, ItemPedido
from usuarios.models import Cliente


def inicial(request):
    produtos = Produto.objects.all()[:6]
    context = {
        'produtos': produtos
    }
    return render(request, 'home.html', context)


def catalogo(request):
    produtos = Produto.objects.all()
    context = {
        'produtos': produtos
    }
    return render(request, 'catalogo.html', context)


def carrinho(request):
    carrinho_session = request.session.get('carrinho', {})
    produtos_carrinho = []
    total = 0

    for produto_id, quantidade in carrinho_session.items():
        produto = Produto.objects.filter(pk=produto_id).first()
        if produto:
            subtotal = produto.preco * quantidade
            total += subtotal
            produtos_carrinho.append({
                'produto': produto,
                'quantidade': quantidade,
                'subtotal': subtotal
            })

    context = {
        'produtos': produtos_carrinho,
        'total': total
    }
    return render(request, 'carrinho.html', context)


def adicionar_carrinho(request, id):
    produto = get_object_or_404(Produto, pk=id)
    carrinho_session = request.session.get('carrinho', {})

    str_id = str(id)
    carrinho_session[str_id] = carrinho_session.get(str_id, 0) + 1

    request.session['carrinho'] = carrinho_session
    messages.success(request, f'{produto.nome} adicionado ao carrinho.')
    return redirect('carrinho')


def remover_carrinho(request, id):
    carrinho_session = request.session.get('carrinho', {})
    str_id = str(id)

    if str_id in carrinho_session:
        if carrinho_session[str_id] > 1:
            carrinho_session[str_id] -= 1
        else:
            del carrinho_session[str_id]

    request.session['carrinho'] = carrinho_session
    messages.success(request, 'Item removido do carrinho.')
    return redirect('carrinho')


@login_required
def pagamento(request):
    carrinho_session = request.session.get('carrinho', {})

    if not carrinho_session:
        messages.error(request, 'Seu carrinho está vazio.')
        return redirect('catalogo')

    cliente = Cliente.objects.filter(usuario=request.user).first()

    if request.method == 'POST':
        forma_pagamento = request.POST.get('forma_pagamento', 'Cartão de Crédito')

        pedido = Pedido.objects.create(
            cliente=cliente,
            status='Concluído'
        )

        for produto_id, quantidade in carrinho_session.items():
            produto = Produto.objects.filter(pk=produto_id).first()
            if produto:
                ItemPedido.objects.create(
                    pedido=pedido,
                    produto=produto,
                    quantidade=quantidade,
                    preco_unitario=produto.preco
                )

                if produto.estoque >= quantidade:
                    produto.estoque -= quantidade
                else:
                    produto.estoque = 0
                produto.save()

        request.session['carrinho'] = {}
        messages.success(request, 'Compra finalizada com sucesso!')
        return redirect('confirmacao', pedido_id=pedido.id)

    produtos_carrinho = []
    total = 0

    for produto_id, quantidade in carrinho_session.items():
        produto = Produto.objects.filter(pk=produto_id).first()
        if produto:
            subtotal = produto.preco * quantidade
            total += subtotal
            produtos_carrinho.append({
                'produto': produto,
                'quantidade': quantidade,
                'subtotal': subtotal
            })

    context = {
        'produtos': produtos_carrinho,
        'total': total,
        'cliente': cliente
    }
    return render(request, 'pagamento.html', context)


@login_required
def confirmacao(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    itens = ItemPedido.objects.filter(pedido=pedido)

    total = sum(item.quantidade * item.preco_unitario for item in itens)

    context = {
        'pedido': pedido,
        'itens': itens,
        'total': total
    }
    return render(request, 'confirmacao.html', context)


def transparencia(request):
    qtd_produtos = Produto.objects.count()
    qtd_categorias = Categoria.objects.count()
    qtd_clientes = Cliente.objects.count()
    qtd_pedidos = Pedido.objects.count()

    precos = Produto.objects.aggregate(
        menor=Min('preco'),
        media=Avg('preco'),
        maior=Max('preco')
    )

    context = {
        'qtd_produtos': qtd_produtos,
        'qtd_categorias': qtd_categorias,
        'qtd_clientes': qtd_clientes,
        'qtd_pedidos': qtd_pedidos,
        'menor_preco': precos['menor'] or 0,
        'media_preco': precos['media'] or 0,
        'maior_preco': precos['maior'] or 0,
    }
    return render(request, 'transparencia.html', context)