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

from .forms import ProdutoForm, CadastroForm, UsuarioForm
from .models import Produto, Cliente, Endereco, Pedido


def inicial(request):
    return render(request, 'home.html')


def catalogo(request):
    produtos = Produto.objects.all()
    return render(request, 'catalogo.html', {'produtos': produtos})


def produto_detalhe(request, id):
    produto = get_object_or_404(Produto, pk=id)
    return render(request, 'produto_detalhe.html', {'produto': produto})


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


def cadastro(request):

    if request.user.is_authenticated:
        return redirect('inicial')

    form = CadastroForm(request.POST or None)

    if request.method == 'POST':

        if form.is_valid():

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            cpf = form.cleaned_data.get('cpf')

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Usuário já existe.')
                return render(request, 'cadastro.html', {'form': form})

            if User.objects.filter(email=email).exists() or Cliente.objects.filter(email=email).exists():
                messages.error(request, 'E-mail já cadastrado.')
                return render(request, 'cadastro.html', {'form': form})

            if cpf and Cliente.objects.filter(cpf=cpf).exists():
                messages.error(request, 'CPF já cadastrado.')
                return render(request, 'cadastro.html', {'form': form})

            usuario = User.objects.create_user(
                username=username,
                email=email,
                password=form.cleaned_data['password']
            )

            data_nascimento = None

            dia = form.cleaned_data.get('dia')
            mes = form.cleaned_data.get('mes')
            ano = form.cleaned_data.get('ano')

            if dia and mes and ano:
                try:
                    data_nascimento = datetime.date(
                        int(ano),
                        int(mes),
                        int(dia)
                    )
                except ValueError:
                    data_nascimento = None

            cliente = Cliente.objects.create(
                usuario=usuario,
                nome=form.cleaned_data['nome'],
                sobrenome=form.cleaned_data['sobrenome'],
                email=email,
                telefone=form.cleaned_data.get('telefone') or '',
                sexo=form.cleaned_data.get('sexo') or '',
                data_nascimento=data_nascimento,
                cpf=cpf or ''
            )

            rua = form.cleaned_data.get('rua')
            cidade = form.cleaned_data.get('cidade')
            estado = form.cleaned_data.get('estado')
            cep = form.cleaned_data.get('cep')

            if rua and cidade and estado and cep:
                Endereco.objects.create(
                    cliente=cliente,
                    rua=rua,
                    numero=form.cleaned_data.get('numero') or '',
                    complemento=form.cleaned_data.get('complemento') or '',
                    bairro=form.cleaned_data.get('bairro') or '',
                    cidade=cidade,
                    estado=estado,
                    cep=cep
                )

            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('login')

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

            return render(request, 'cadastro.html', {'form': form})

    return render(request, 'cadastro.html', {'form': form})


def login(request):
    if request.user.is_authenticated:
        return redirect('inicial')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        usuario = authenticate(request, username=username, password=password)

        if usuario is not None:
            auth_login(request, usuario)
            return redirect('inicial')

        messages.error(request, 'Usuário ou senha inválidos.')

    return render(request, 'login.html')


@login_required
def logout(request):
    auth_logout(request)
    return redirect('inicial')


@login_required
def produtos(request):
    produtos = Produto.objects.all()
    context = {
    'produtos': produtos,
     "pagina": "produtos",
    }
    return render(request, 'privado/produtos.html', context)


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
def painel(request):

    total_produtos = Produto.objects.count()
    total_clientes = Cliente.objects.count()
    total_pedidos = Pedido.objects.count()

    estoque_total = Produto.objects.aggregate(
        total=Sum("estoque")
    )["total"] or 0

    context = {
        "total_produtos": total_produtos,
        "total_clientes": total_clientes,
        "total_pedidos": total_pedidos,
        "estoque_total": estoque_total,
        "pagina": "painel",
    }

    return render(request, "privado/painel.html", context)


@login_required
def usuarios(request):
    lista = User.objects.all()

    context = {
        "pagina": "usuarios",
        "usuarios": lista,
    }

    return render(request, "privado/usuarios.html", context)

@login_required
def add_usuario(request):

    form = UsuarioForm(request.POST or None)

    print(request.user.username)
    print(form.initial)

    context = {
        "pagina": "usuarios_1",
        "form": form,
    }

    if request.method == "POST":

        if form.is_valid():

            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]

            if User.objects.filter(username=username).exists():
                messages.error(request, "Usuário já existe.")
                return render(request, "privado/add_usuario.html", context)

            if User.objects.filter(email=email).exists():
                messages.error(request, "E-mail já cadastrado.")
                return render(request, "privado/add_usuario.html", context)

            usuario = User.objects.create_user(
                username=username,
                email=email,
                password=form.cleaned_data["password"]
            )

            Cliente.objects.create(
                usuario=usuario,
                nome=form.cleaned_data["nome"],
                sobrenome=form.cleaned_data["sobrenome"],
                cpf=form.cleaned_data.get("cpf") or "",
                telefone=form.cleaned_data.get("telefone") or "",
                sexo=form.cleaned_data.get("sexo") or "",
                email=email
            )

            messages.success(request, "Usuário cadastrado com sucesso.")
            return redirect("usuarios")

    return render(request, "privado/add_usuario.html", context)


@login_required
def usuario_editar(request, id):
    usuario = get_object_or_404(User, pk=id)

    cliente = Cliente.objects.filter(usuario=usuario).first()

    endereco = None
    if cliente:
        endereco = Endereco.objects.filter(cliente=cliente).first()

    dados = {
        "username": usuario.username,
        "email": usuario.email,

        "nome": cliente.nome if cliente else "",
        "sobrenome": cliente.sobrenome if cliente else "",
        "cpf": cliente.cpf if cliente else "",
        "telefone": cliente.telefone if cliente else "",
        "sexo": cliente.sexo if cliente else "",

        "cep": endereco.cep if endereco else "",
        "estado": endereco.estado if endereco else "",
        "cidade": endereco.cidade if endereco else "",
        "bairro": endereco.bairro if endereco else "",
        "rua": endereco.rua if endereco else "",
        "numero": endereco.numero if endereco else "",
        "complemento": endereco.complemento if endereco else "",
    }

    form = UsuarioForm(
        request.POST or None,
        initial=dados
    )

    if request.method == "POST":

        if form.is_valid():

            usuario.username = form.cleaned_data["username"]
            usuario.email = form.cleaned_data["email"]
            usuario.save()

            if cliente:
                cliente.nome = form.cleaned_data["nome"]
                cliente.sobrenome = form.cleaned_data["sobrenome"]
                cliente.cpf = form.cleaned_data["cpf"]
                cliente.telefone = form.cleaned_data["telefone"]
                cliente.sexo = form.cleaned_data["sexo"]
                cliente.save()

            messages.success(request, "Usuário atualizado com sucesso.")
            return redirect("usuarios")

    context = {
        "pagina": "usuarios_1",
        "form": form,
    }

    return render(request, "privado/add_usuario.html", context)

@login_required
def usuario_delete(request, id):
    usuario = get_object_or_404(User, pk=id)
    usuario.delete()
    messages.success(request, 'Usuário removido.')
    return redirect('usuarios')

@login_required
def meus_dados(request):
    context = {
     "pagina": "meus_dados",
    }
    return render(request, 'privado/meus_dados.html', context)


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

 