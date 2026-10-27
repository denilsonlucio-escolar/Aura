import io
import os
from pathlib import Path
from PIL import Image
from django.core.files.base import ContentFile
from produtos.models import Produto

# Caminho da pasta onde você baixou as fotos
PASTA_ORIGEM = Path(r"C:\Users\João Guilherme\imagens aura")

# Mapeamento com nomes profissionais, descrições e dados para o SIG/SAD
DADOS_PRODUTOS = [
    {
        "arquivo": "bola.png",
        "busca": "Bola",
        "nome": "Bola de Futebol Pro Aura",
        "descricao": "Bola oficial de campo termo-colada, revestimento em PU de alta durabilidade e câmara de látex.",
        "preco": 129.90,
        "estoque": 15,
    },
    {
        "arquivo": "chuteira.png",
        "busca": "Chuteira",
        "nome": "Chuteira Campo Elite Aura",
        "descricao": "Chuteira com travas multidirecionais, cabedal em material sintético reforçado e ajuste anatômico.",
        "preco": 249.90,
        "estoque": 8,
    },
    {
        "arquivo": "shorts.png",
        "busca": "Shorts",
        "nome": "Shorts de Corrida Breathable Aura",
        "descricao": "Shorts leve em poliéster com secagem rápida, cós elástico com cordão e bolso interno.",
        "preco": 59.90,
        "estoque": 3,
    },
    {
        "arquivo": "tenis.png",
        "busca": "Tênis",
        "nome": "Tênis Running Air Aura",
        "descricao": "Tênis com tecnologia de amortecimento a ar, cabedal respirável em mesh e solado antiderrapante.",
        "preco": 329.90,
        "estoque": 12,
    },
    {
        "arquivo": "garrafa.png",
        "busca": "Garrafa",
        "nome": "Garrafa Térmica Inox 1L Aura",
        "descricao": "Garrafa em aço inoxidável com parede dupla a vácuo. Conserva bebidas geladas por até 24 horas.",
        "preco": 89.90,
        "estoque": 4,
    },
    {
        "arquivo": "luva.png",
        "busca": "Luva",
        "nome": "Luva de Goleiro Grip Aura",
        "descricao": "Luva profissional com látex natural de 4mm, corte negativo para maior sensibilidade e fecho duplo.",
        "preco": 119.90,
        "estoque": 2,
    },
    {
        "arquivo": "mochila.png",
        "busca": "Mochila",
        "nome": "Mochila Esportiva Impermeável Aura",
        "descricao": "Mochila reforçada com compartimento isolado para calçados, tiras acolchoadas e tecido impermeável.",
        "preco": 149.90,
        "estoque": 18,
    },
    {
        "arquivo": "caneleira.png",
        "busca": "Caneleira",
        "nome": "Caneleira Forte Guard Aura",
        "descricao": "Proteção de polipropileno rígido com revestimento interno em EVA para alta absorção de impactos.",
        "preco": 39.90,
        "estoque": 1,
    },
    {
        "arquivo": "meiao.png",
        "busca": "Meião",
        "nome": "Meião Anatômico Pro Aura",
        "descricao": "Meião em algodão e poliamida com compressão no tornozelo e calcanhar reforçado.",
        "preco": 29.90,
        "estoque": 30,
    },
]

def executar():
    print("Iniciando o processamento das imagens e atualização dos produtos...\n")
    for item in DADOS_PRODUTOS:
        caminho_img = PASTA_ORIGEM / item["arquivo"]
        if not caminho_img.exists():
            print(f"⚠️ Imagem não encontrada: {item['arquivo']}")
            continue

        # 1. Trata a imagem: Fundo Branco + Tela 400x400 centralizada
        img_original = Image.open(caminho_img).convert("RGBA")
        
        # Cria um quadrado em branco de 400x400
        canvas = Image.new("RGBA", (400, 400), (255, 255, 255, 255))
        
        # Redimensiona mantendo a proporção (máximo 350px para dar 25px de borda/respiro)
        img_original.thumbnail((350, 350), Image.Resampling.LANCZOS)
        
        # Centraliza a imagem no canvas
        x = (400 - img_original.width) // 2
        y = (400 - img_original.height) // 2
        canvas.paste(img_original, (x, y), img_original)
        
        # Converte para RGB simples (fundo branco impresso)
        canvas_rgb = canvas.convert("RGB")
        
        # Converte a imagem tratada para bytes para salvar no Django
        buffer = io.BytesIO()
        canvas_rgb.save(buffer, format="JPEG", quality=95)
        nome_arquivo_final = f"{Path(item['arquivo']).stem}_aura.jpg"

        # 2. Atualiza ou cria o produto no banco de dados do Django
        prod = Produto.objects.filter(nome__icontains=item["busca"]).first()
        if not prod:
            prod = Produto(nome=item["nome"])

        prod.nome = item["nome"]
        prod.descricao = item["descricao"]
        prod.estoque = item["estoque"]
        
        if hasattr(prod, 'preco'):
            prod.preco = item["preco"]
        elif hasattr(prod, 'preco_unitario'):
            prod.preco_unitario = item["preco"]

        # Salva o arquivo de imagem no ImageField
        prod.imagem.save(nome_arquivo_final, ContentFile(buffer.getvalue()), save=False)
        prod.save()

        print(f"✅ Product '{prod.nome}' atualizado com imagem formatada!")

    print("\n>>> Processamento concluído com sucesso!")

executar()