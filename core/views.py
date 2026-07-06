from django.shortcuts import render, redirect
from .forms import ProdutoForm
from .models import Produto



def inicial(request):
    return render(request, 'home.html')

def cadastro(request):
    return render(request, 'cadastro.html')

def carrinho(request):
    return render(request, 'carrinho.html')

def login(request):
    return render(request, 'login.html')

def pagamento(request):
    return render(request, 'pagamento.html')

def catalogo(request):
    produtos = Produto.objects.all()
    context = {
        'produtos': produtos
    }
    return render(request, 'catalogo.html', context)

def produtos(request):
    produtos = Produto.objects.all()
    context = {
        'produtos': produtos
    }
    return render(request, 'privado/produtos.html', context)


def add_produtos(request):
    form = ProdutoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('produtos')
    else:
        print(form.errors)
    context = {
        'form': form
    }
    return render(request, 'privado/add_produtos.html', context)

def produto_delete(request, id):
    produto = Produto.objects.get(pk=id)
    produto.delete()
    return redirect('produtos')

def produto_editar(request, id):
    produto = Produto.objects.get(pk=id)
    form = ProdutoForm(request.POST or None, instance=produto)
    if form.is_valid():
        form.save()
        return redirect('produtos')
    context = {
        'form' : form
        
    }

    return render (request, 'privado/add_produtos.html', context)





