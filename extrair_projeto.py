"""
extrair_projeto.py
Extrai a estrutura completa + código-fonte de um projeto Django para um único arquivo .txt.

Uso:
    python extrair_projeto.py
    python extrair_projeto.py "C:\\caminho\\do\\projeto"
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# ============================================================
# CONFIGURAÇÕES — ajuste conforme necessário
# ============================================================

OUTPUT_FILE = "estrutura_projeto.txt"

# Extensões de código-fonte que DEVEM ser incluídas
INCLUDE_EXTENSIONS = {
    # Código
    '.py', '.html', '.htm', '.css', '.js', '.jsx', '.ts', '.tsx',
    '.sql', '.json', '.yml', '.yaml',
    # Documentação / texto
    '.txt', '.md', '.rst',
    # Dados
    '.csv',
}

# Pastas que devem ser IGNORADAS completamente
EXCLUDE_DIRS = {
    '.git', '.github', '.gitlab',
    '.idea', '.vscode', '.vs',
    '__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache',
    'node_modules', 'bower_components',
    '.venv', 'venv', 'env', 'ENV',
    'dist', 'build', 'egg-info',
    'media', 'staticfiles', 'logs', 'tmp',
    '.migrations_backup',
    'migrations',  # autogeradas pelo Django — ruído, não conteúdo útil
}

# Arquivos específicos a ignorar (por nome)
EXCLUDE_FILES = {
    'db.sqlite3', 'db.sqlite3-journal',
    'package-lock.json', 'yarn.lock', 'poetry.lock', 'Pipfile.lock',
    '.DS_Store', 'Thumbs.db', 'desktop.ini',
    '.env', '.env.local', '.env.production',
}

# Trechos que, se presentes no nome do arquivo, indicam biblioteca de
# terceiros vendorizada (ex: bootstrap.min.css, jquery.min.js) — não é
# código do projeto, então é ignorado mesmo tendo extensão permitida
EXCLUDE_NAME_SUBSTRINGS = {
    '.min.',
}

# Tamanho máximo por arquivo (500 KB) — evita travar com arquivos enormes
MAX_FILE_SIZE = 500 * 1024

# ============================================================
# LÓGICA
# ============================================================

def should_exclude_dir(name: str) -> bool:
    return name in EXCLUDE_DIRS or name.startswith('.')


def should_exclude_file(path: Path) -> bool:
    if path.name in EXCLUDE_FILES:
        return True
    if any(sub in path.name for sub in EXCLUDE_NAME_SUBSTRINGS):
        return True
    if path.suffix.lower() not in INCLUDE_EXTENSIONS:
        return True
    try:
        if path.stat().st_size > MAX_FILE_SIZE:
            return True
        if path.stat().st_size == 0:
            return True
    except OSError:
        return True
    return False


def build_tree(root: Path) -> str:
    """Gera representação visual em árvore do projeto."""
    lines = [root.name + "/"]

    def walk(current: Path, prefix: str = ""):
        try:
            entries = sorted(
                current.iterdir(),
                key=lambda e: (e.is_file(), e.name.lower())
            )
        except PermissionError:
            return

        entries = [
            e for e in entries
            if not (e.is_dir() and should_exclude_dir(e.name))
            and not (e.is_file() and should_exclude_file(e))
        ]

        for i, entry in enumerate(entries):
            is_last = (i == len(entries) - 1)
            connector = "└── " if is_last else "├── "
            lines.append(f"{prefix}{connector}{entry.name}")

            if entry.is_dir():
                extension = "    " if is_last else "│   "
                walk(entry, prefix + extension)

    walk(root)
    return "\n".join(lines)


def extract_files(root: Path, output):
    """Percorre o projeto e escreve o conteúdo de cada arquivo relevante."""
    total_files = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not should_exclude_dir(d)]

        for filename in sorted(filenames):
            file_path = Path(dirpath) / filename
            if should_exclude_file(file_path):
                continue

            rel = file_path.relative_to(root)
            output.write("\n" + "=" * 90 + "\n")
            output.write(f"ARQUIVO: {rel}\n")
            output.write("=" * 90 + "\n")

            try:
                content = file_path.read_text(encoding='utf-8', errors='replace')
                output.write(content)
                if not content.endswith('\n'):
                    output.write('\n')
                total_files += 1
                print(f"  ✓ {rel}")
            except Exception as e:
                output.write(f"[ERRO AO LER ARQUIVO: {e}]\n")

    return total_files


def main():
    # Define raiz do projeto
    if len(sys.argv) > 1:
        root = Path(sys.argv[1]).resolve()
    else:
        root = Path.cwd()

    if not root.is_dir():
        print(f"❌ Caminho inválido: {root}")
        sys.exit(1)

    print(f"📁 Projeto: {root}")
    print(f"📄 Saída:   {OUTPUT_FILE}")
    print("─" * 60)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        # Cabeçalho
        f.write("#" * 90 + "\n")
        f.write("# EXTRAÇÃO COMPLETA DO PROJETO\n")
        f.write(f"# Raiz do projeto: {root}\n")
        f.write(f"# Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("#" * 90 + "\n\n")

        # Parte 1 — Árvore de diretórios
        f.write("=" * 90 + "\n")
        f.write("PARTE 1 — ESTRUTURA DE DIRETÓRIOS\n")
        f.write("=" * 90 + "\n\n")
        f.write(build_tree(root))
        f.write("\n\n\n")

        # Parte 2 — Conteúdo dos arquivos
        f.write("=" * 90 + "\n")
        f.write("PARTE 2 — CONTEÚDO DOS ARQUIVOS\n")
        f.write("=" * 90 + "\n")
        total = extract_files(root, f)

    size_mb = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
    print("─" * 60)
    print(f"✅ Arquivo gerado: {OUTPUT_FILE}")
    print(f"📦 Tamanho: {size_mb:.2f} MB")
    print(f"📄 Total de arquivos incluídos: {total}")


if __name__ == "__main__":
    main()
