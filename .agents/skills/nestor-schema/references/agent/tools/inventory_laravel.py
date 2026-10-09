#!/usr/bin/env python3
"""Nestor Schema: inventário heurístico *somente leitura* de fontes PHP Laravel.

Não conecta a bancos, não executa Artisan, Composer ou código PHP.
Busca textual, não AST: achados precisam de confirmação pelo Nestor Reader.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess
import sys

PATTERNS = [
    ('migration_create', re.compile(r"\bSchema\s*::\s*create\s*\(\s*['\"]([A-Za-z_][\w.]*)['\"]")),
    ('migration_alter', re.compile(r"\bSchema\s*::\s*table\s*\(\s*['\"]([A-Za-z_][\w.]*)['\"]")),
    ('migration_drop', re.compile(r"\bSchema\s*::\s*(?:drop|dropIfExists)\s*\(\s*['\"]([A-Za-z_][\w.]*)['\"]")),
    ('eloquent_model', re.compile(r"\bclass\s+(\w+)\s+extends\s+Model\b")),
    ('eloquent_relation', re.compile(r"\$this\s*->\s*(belongsToMany|belongsTo|hasMany|hasOne|morphTo|morphMany|morphOne|morphToMany|hasManyThrough|hasOneThrough)\s*\(")),
    ('db_table_usage', re.compile(r"\bDB\s*::\s*table\s*\(\s*['\"]([A-Za-z_][\w.]*)['\"]")),
    ('laravel_route', re.compile(r"\bRoute\s*::\s*(get|post|put|patch|delete|resource|apiResource)\s*\(")),
]
SCAN_PATHS = ('app', 'database/migrations', 'database/factories', 'routes')
EXCLUDE_PARTS = {'.git', 'vendor', 'node_modules', 'storage', 'bootstrap/cache', '.venv', 'tests'}


def git_head(root: Path) -> str:
    try:
        res = subprocess.run(['git', '-C', str(root), 'rev-parse', 'HEAD'], capture_output=True,
                             text=True, timeout=3, check=False)
        sha = res.stdout.strip()
        return sha if res.returncode == 0 and re.fullmatch(r'[0-9a-f]{40,64}', sha) else 'UNKNOWN'
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return 'UNKNOWN'


def inventory(root: Path, max_files: int = 5000, max_bytes: int = 2_000_000) -> dict:
    root = root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError('Raiz precisa ser um diretório')
    if max_files < 1 or max_bytes < 1:
        raise ValueError('Limites devem ser positivos')
    evidence, findings, gaps = [], [], []
    candidates: list[Path] = []
    for sub in SCAN_PATHS:
        directory = root / sub
        if directory.is_dir() and not directory.is_symlink():
            for path in directory.rglob('*.php'):
                if path.is_symlink() or not path.is_file():
                    continue
                relative = path.relative_to(root)
                if any(part in EXCLUDE_PARTS for part in relative.parts):
                    continue
                candidates.append(path)
    candidates = sorted(set(candidates), key=lambda p: p.as_posix())
    if len(candidates) > max_files:
        gaps.append(f'Limite de {max_files} arquivos: inventário parcial ({len(candidates)} encontrados).')
        candidates = candidates[:max_files]
    for file in candidates:
        relative = file.relative_to(root).as_posix()
        try:
            if file.stat().st_size > max_bytes:
                gaps.append(f'Arquivo ignorado por tamanho: {relative}')
                continue
            raw = file.read_text(encoding='utf-8', errors='replace')
        except OSError:
            gaps.append(f'Falha de leitura: {relative}')
            continue
        for kind, pattern in PATTERNS:
            for match in pattern.finditer(raw):
                # Texto com comentários ou strings pode gerar falsos positivos: achado é sintático/heurístico.
                symbol = match.group(1)
                line = raw.count('\n', 0, match.start()) + 1
                ident = f'e{len(evidence)+1}'
                evidence.append({
                    'id': ident, 'path': relative, 'line': line, 'symbol': symbol,
                    'label': 'FACT',
                    'observation': f'Expressão textual compatível com {kind}: {symbol}. Não comprova execução nem schema físico.',
                    'method': 'static-text',
                })
                findings.append({
                    'id': f'f{len(findings)+1}', 'kind': kind, 'symbol': symbol,
                    'description': f'Padrão sintático encontrado para {kind}; validar o contexto PHP e a estrutura real.',
                    'evidence_refs': [ident], 'label': 'FACT',
                })
    gaps.extend([
        'Inventário baseado em regex: não é parser PHP/AST, pode capturar comentários ou omitir chamadas dinâmicas.',
        'Não houve conexão ou introspecção de PostgreSQL: tabelas físicas e constraints permanecem desconhecidas.',
        'Confirmar cardinalidade, ownership e regras de negócio no código e com Nestor Reader.',
    ])
    return {
        'schema_version': '1.0', 'producer': 'nestor-schema-static-inventory',
        'repository': str(root), 'commit': git_head(root),
        'generated_at': datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'evidence': evidence, 'findings': findings, 'gaps': gaps,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True, help='Diretório raiz do repositório Laravel')
    parser.add_argument('--output', type=Path, help='Arquivo JSON de saída (padrão: stdout)')
    parser.add_argument('--max-files', type=int, default=5000)
    args = parser.parse_args(argv)
    try:
        report = inventory(args.root, args.max_files)
        payload = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(payload, encoding='utf-8')
        else:
            sys.stdout.write(payload)
        return 0
    except (OSError, ValueError) as exc:
        parser.exit(2, f'Erro: {exc}\n')


if __name__ == '__main__':
    raise SystemExit(main())
