from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Produto, Categoria
from .forms import ProdutoForm, CategoriaForm

def produto_detalhe(request, id):
    produto = get_object_or_404(Produto, pk=id)
    return render(request, 'produto_detalhe.html', {'produto': produto})

@login_required
def produto_editar(request, id):
    produto = get_object_or_404(Produto, pk=id)
    form = ProdutoForm(request.POST or None, request.FILES or None, instance=produto)

    context = {
     "pagina": "produtos_1",
     'form': form
    }

    if form.is_valid():
        form.save()
        messages.success(request, 'Produto atualizado.')
        return redirect('produtos')

    return render(request, 'privado/add_produtos.html', context)


@login_required
def produto_delete(request, id):
    produto = get_object_or_404(Produto, pk=id)
    produto.delete()
    messages.success(request, 'Produto removido.')
    return redirect('produtos')


@login_required
def add_produtos(request):
    form = ProdutoForm(request.POST or None, request.FILES or None)

    context = {
     "pagina": "produtos_1",
     'form': form
    }

    if form.is_valid():
        form.save()
        messages.success(request, 'Produto cadastrado.')
        return redirect('produtos')

    return render(request, 'privado/add_produtos.html', context)

@login_required
def produtos(request):
    produtos = Produto.objects.all()
    context = {
    'produtos': produtos,
     "pagina": "produtos",
    }
    return render(request, 'privado/produtos.html', context)

@login_required
def add_categoria(request):
    form = CategoriaForm(request.POST or None)

    context = {
     "pagina": "categorias",
     'form': form
    }

    if form.is_valid():
        form.save()
        messages.success(request, 'Categoria cadastrada com sucesso.')
        return redirect('produtos')

    return render(request, 'privado/add_categoria.html', context)

@login_required
def categoria_delete(request, id):
    Categoria = get_object_or_404(Categoria, pk=id)
    Categoria.delete()
    messages.success(request, 'Categoria removida.')
    return redirect('categoria')


@login_required
def categoria_editar(request, id):
    categoria = get_object_or_404(Categoria, pk=id)
    form = CategoriaForm(request.POST or None, instance=categoria)

    context = {
     "pagina": "categoria_1",
     'form': form
    }

    if form.is_valid():
        form.save()
        messages.success(request, 'categoria atualizada.')
        return redirect('Categoria')

    return render(request, 'privado/add_categoria.html', context)
