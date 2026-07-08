import datetime

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import ProdutoForm, CadastroForm, UsuarioForm
from .models import Produto, Cliente, Endereco


def inicial(request):
    return render(request, 'home.html')


def catalogo(request):
    produtos = Produto.objects.all()
    return render(request, 'catalogo.html', {'produtos': produtos})


def produto_detalhe(request, id):
    produto = get_object_or_404(Produto, pk=id)
    return render(request, 'produto_detalhe.html', {'produto': produto})


def carrinho(request):
    return render(request, 'carrinho.html')


def pagamento(request):
    return render(request, 'pagamento.html')


def cadastro(request):
    if request.user.is_authenticated:
        return redirect('inicial')

    form = CadastroForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            cpf = form.cleaned_data.get('cpf')

            # 1. Checa se o username já existe no User
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Nome de usuário já existe.')
                return render(request, 'cadastro.html', {'form': form})

            # 2. Checa se o e-mail já existe no User OU no Cliente
            if email and (User.objects.filter(email=email).exists() or Cliente.objects.filter(email=email).exists()):
                messages.error(request, 'E-mail já cadastrado.')
                return render(request, 'cadastro.html', {'form': form})
            
            # 3. Checa se o CPF já existe no Cliente
            if cpf and Cliente.objects.filter(cpf=cpf).exists():
                messages.error(request, 'CPF já cadastrado.')
                return render(request, 'cadastro.html', {'form': form})

            # Se passou em todas as checagens, cria o usuário
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
                senha='',
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

            return redirect(f"{reverse('login')}?cadastro=sucesso")
        
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    nome_campo = field.capitalize() if field != '__all__' else 'Erro'
                    messages.error(request, f"{nome_campo}: {error}")

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
    return redirect('login')


@login_required
def produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'privado/produtos.html', {'produtos': produtos})


@login_required
def add_produtos(request):
    form = ProdutoForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Produto cadastrado.')
        return redirect('produtos')

    return render(request, 'privado/add_produtos.html', {'form': form})


@login_required
def produto_editar(request, id):
    produto = get_object_or_404(Produto, pk=id)
    form = ProdutoForm(request.POST or None, request.FILES or None, instance=produto)

    if form.is_valid():
        form.save()
        messages.success(request, 'Produto atualizado.')
        return redirect('produtos')

    return render(request, 'privado/add_produtos.html', {'form': form})


@login_required
def produto_delete(request, id):
    produto = get_object_or_404(Produto, pk=id)
    produto.delete()
    messages.success(request, 'Produto removido.')
    return redirect('produtos')


@login_required
def painel(request):
    return render(request, 'privado/painel.html')


@login_required
def usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'privado/usuarios.html', {'usuarios': usuarios})


@login_required
def usuario_editar(request, id):
    usuario = get_object_or_404(User, pk=id)
    form = UsuarioForm(request.POST or None, instance=usuario)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário atualizado.')
            return redirect('usuarios')
        else:
            # Se der erro de validação, pega os erros e manda para a tela
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")

    return render(request, 'privado/add_usuario.html', {'form': form})


@login_required
def usuario_delete(request, id):
    usuario = get_object_or_404(User, pk=id)
    usuario.delete()
    messages.success(request, 'Usuário removido.')
    return redirect('usuarios')