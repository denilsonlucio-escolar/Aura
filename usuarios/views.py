import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum, F, DecimalField

from .forms import CadastroForm, UsuarioForm
from .models import Cliente, Endereco
from produtos.models import Produto, Categoria
from pedidos.models import Pedido, ItemPedido


def staff_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_staff:
            messages.error(request, 'Acesso restrito a administradores.')
            return redirect('meus_dados')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


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
                    data_nascimento = datetime.date(int(ano), int(mes), int(dia))
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


@staff_required
def painel(request):
    total_produtos = Produto.objects.count()
    total_clientes = Cliente.objects.count()
    total_pedidos = Pedido.objects.count()
    total_categorias = Categoria.objects.count()

    estoque_total = Produto.objects.aggregate(
        total=Sum("estoque")
    )["total"] or 0

    # --- SIG: CÁLCULOS GERENCIAIS ---
    faturamento_total = ItemPedido.objects.aggregate(
        total=Sum(F('quantidade') * F('preco_unitario'), output_field=DecimalField())
    )['total'] or 0

    ticket_medio = (faturamento_total / total_pedidos) if total_pedidos > 0 else 0

    top_produto_item = ItemPedido.objects.values('produto__nome').annotate(
        total_vendido=Sum('quantidade')
    ).order_by('-total_vendido').first()

    top_produto_nome = top_produto_item['produto__nome'] if top_produto_item else "Nenhum pedido"
    top_produto_qtd = top_produto_item['total_vendido'] if top_produto_item else 0

    # --- SAD: ALERTAS INTELIGENTES ---
    produtos_estoque_baixo = Produto.objects.filter(estoque__lte=5)
    qtd_estoque_baixo = produtos_estoque_baixo.count()

    alertas_reabastecimento = []
    for p in produtos_estoque_baixo:
        alertas_reabastecimento.append({
            'produto': p,
            'qtd_sugerida_comprar': max(20 - p.estoque, 10)
        })

    # CORREÇÃO AQUI: 'itens__isnull=True' utiliza o related_name 'itens' do model ItemPedido
    produtos_sem_giro = Produto.objects.filter(itens__isnull=True, estoque__gt=0)

    context = {
        "total_produtos": total_produtos,
        "total_clientes": total_clientes,
        "total_categorias": total_categorias,
        "total_pedidos": total_pedidos,
        "estoque_total": estoque_total,
        "faturamento_total": faturamento_total,
        "ticket_medio": ticket_medio,
        "top_produto_nome": top_produto_nome,
        "top_produto_qtd": top_produto_qtd,
        "produtos_estoque_baixo": produtos_estoque_baixo,
        "qtd_estoque_baixo": qtd_estoque_baixo,
        "alertas_reabastecimento": alertas_reabastecimento,
        "produtos_sem_giro": produtos_sem_giro,
        "pagina": "painel",
    }

    return render(request, "privado/painel.html", context)


@staff_required
def usuarios(request):
    lista = User.objects.all()

    context = {
        "pagina": "usuarios",
        "usuarios": lista,
    }

    return render(request, "privado/usuarios.html", context)


@staff_required
def add_usuario(request):
    form = UsuarioForm(request.POST or None)

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


@staff_required
def usuario_delete(request, id):
    usuario = get_object_or_404(User, pk=id)
    usuario.delete()
    messages.success(request, 'Usuário removido.')
    return redirect('usuarios')


@staff_required
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
def meus_dados(request):
    cliente = Cliente.objects.filter(usuario=request.user).first()
    endereco = Endereco.objects.filter(cliente=cliente).first() if cliente else None

    if request.method == 'POST':
        if cliente:
            cliente.nome = request.POST.get('nome', cliente.nome)
            cliente.sobrenome = request.POST.get('sobrenome', cliente.sobrenome)
            cliente.telefone = request.POST.get('telefone', cliente.telefone)
            cliente.cpf = request.POST.get('cpf', cliente.cpf)
            cliente.save()

            if endereco:
                endereco.rua = request.POST.get('rua', endereco.rua)
                endereco.numero = request.POST.get('numero', endereco.numero)
                endereco.bairro = request.POST.get('bairro', endereco.bairro)
                endereco.cidade = request.POST.get('cidade', endereco.cidade)
                endereco.estado = request.POST.get('estado', endereco.estado)
                endereco.cep = request.POST.get('cep', endereco.cep)
                endereco.save()
            elif request.POST.get('cep'):
                Endereco.objects.create(
                    cliente=cliente,
                    rua=request.POST.get('rua', ''),
                    numero=request.POST.get('numero', ''),
                    bairro=request.POST.get('bairro', ''),
                    cidade=request.POST.get('cidade', ''),
                    estado=request.POST.get('estado', ''),
                    cep=request.POST.get('cep', '')
                )

            messages.success(request, 'Seus dados foram atualizados com sucesso!')
            return redirect('meus_dados')

    context = {
        'cliente': cliente,
        'endereco': endereco,
        'pagina': 'meus_dados'
    }
    return render(request, 'privado/meus_dados.html', context)