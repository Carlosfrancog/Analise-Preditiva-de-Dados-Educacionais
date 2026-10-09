#!/usr/bin/env python3
"""Inventário determinístico e conservador. Nunca executa comandos Docker de mutação.

--offline: nomes/tamanhos de arquivos conhecidos (não lê conteúdos/secrets).
--live: metadados limitados de Docker usando comandos de leitura predefinidos.
Saída JSON. Não utiliza shell=True, não inspeciona env, mounts privados ou logs.
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ALLOWED_NAMES = {'Dockerfile', 'docker-compose.yml', 'docker-compose.yaml', 'compose.yml', 'compose.yaml', '.dockerignore'}
SKIP_DIRS = {'.git', 'node_modules', '.venv', 'vendor', 'dist', 'build', '.next', '.idea', 'target'}
SENSITIVE_FILE = re.compile(r'(^|/)(\.env(?:\..*)?|[^/]*(?:secret|private|credential|keypair|id_rsa)[^/]*)$', re.I)
MAX_FILES = 250

def utc_now():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def subprocess_read(args: list[str], *, timeout=12) -> str:
    # Lista estática construída internamente. Sem shell, sem comandos vindos de configuração.
    p = subprocess.run(args, capture_output=True, text=True, timeout=timeout, check=False)
    if p.returncode:
        raise RuntimeError(f'{args[0]} {args[1] if len(args)>1 else ""} indisponível (status {p.returncode})')
    return p.stdout.strip()

def offline_files(root: Path):
    found=[]
    if not root.is_dir():
        raise ValueError('O caminho --offline deve ser uma pasta existente')
    for current, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith('.cache'))
        for name in sorted(files):
            rel = (Path(current)/name).relative_to(root).as_posix()
            if SENSITIVE_FILE.search(rel):
                continue
            if name not in ALLOWED_NAMES and not (name.startswith('Dockerfile.') and re.fullmatch(r'[A-Za-z0-9_.-]+', name)):
                continue
            try:
                size = (Path(current)/name).stat().st_size
            except OSError:
                continue
            found.append({'path':rel, 'kind':'docker_definition', 'bytes':size})
            if len(found) >= MAX_FILES:
                return found, True
    return found, False

def live_metadata(expected_context: str, project: str):
    context=subprocess_read(['docker','context','show'])
    if context != expected_context:
        raise ValueError('O contexto Docker ativo não corresponde ao --expected-context')
    ver = subprocess_read(['docker','version','--format','{{.Server.Version}}'])
    # Escopo restrito ao projeto Compose explicitamente informado.
    # Sem inspeção detalhada: variáveis, labels e mounts não são exportados.
    out = subprocess_read(['docker','ps','-a','--filter',f'label=com.docker.compose.project={project}','--format','{{json .}}'])
    result=[]
    for line in out.splitlines():
        try:
            row=json.loads(line)
            result.append({'name':row.get('Names',''), 'state':row.get('Status'),
                           'image':row.get('Image'), 'health':None})
        except json.JSONDecodeError:
            continue
    try:
        compose_ver=subprocess_read(['docker','compose','version','--short'])
    except (RuntimeError,FileNotFoundError,subprocess.TimeoutExpired):
        compose_ver=None
    return ver,compose_ver,context,result

def parse_args(argv=None):
    ap=argparse.ArgumentParser(description='Inventário Docker sem ações de mutação e sem ler secrets')
    ap.add_argument('--offline',type=Path,help='Pasta de repositório para inspecionar apenas nomes/tamanhos de definições Docker')
    ap.add_argument('--live',action='store_true',help='Consultar explicitamente metadados Docker de leitura (containers do contexto ativo)')
    ap.add_argument('--environment',choices=['dev','test','homolog','prod','unknown'],default='unknown')
    ap.add_argument('--project', help='Projeto Docker Compose a inspecionar (obrigatório em --live)')
    ap.add_argument('--expected-context', help='Contexto Docker explicitamente confirmado (obrigatório em --live)')
    ns=ap.parse_args(argv)
    if ns.live and (not ns.project or not ns.expected_context):
        ap.error('--live exige --project e --expected-context para limitar o alvo')
    return ns

def build_inventory(ns):
    inv={'schema_version':'1.0','environment':ns.environment,
         'collection_mode':'hybrid' if ns.live and ns.offline else ('live' if ns.live else 'offline'),
         'docker_context':None,'collected_at':utc_now(),
         'engine_version':None,'compose_version':None,
         'services':[],'files':[],'evidence':[],'limitations':[]}
    if ns.offline:
        inv['files'],truncated=offline_files(ns.offline)
        inv['evidence'].append({'label':'FACT','statement':'Inventário por nomes e tamanhos de arquivos; conteúdo não lido','source':'filesystem','collected_at':inv['collected_at'],'context':'offline','confidence':'confirmed'})
        if truncated:
            inv['limitations'].append('Limite de 250 arquivos; inventário truncado')
    if ns.live:
        try:
            v,c,ctx,services=live_metadata(ns.expected_context,ns.project)
            inv.update(engine_version=v,compose_version=c,docker_context=ctx,services=services)
            inv['evidence'].append({'label':'FACT','statement':'Metadados de containers consultados em modo somente leitura','source':'docker CLI','collected_at':inv['collected_at'],'context':'live','confidence':'confirmed'})
        except (ValueError,RuntimeError,FileNotFoundError,subprocess.TimeoutExpired) as exc:
            inv['limitations'].append(f'Docker indisponível ou consulta falhou: {type(exc).__name__}')
    if not ns.offline and not ns.live:
        inv['limitations'].append('Nenhuma coleta solicitada; utilize --offline e/ou --live explicitamente')
    inv['limitations'].append('Não consulta logs, env, mounts detalhados, secrets, métricas ou readiness da aplicação')
    return inv

def main(argv=None):
    ns=parse_args(argv)
    try:
        print(json.dumps(build_inventory(ns),ensure_ascii=False,indent=2))
        return 0
    except (ValueError,OSError) as exc:
        print(f'Erro de entrada: {type(exc).__name__}', file=sys.stderr)
        return 2

if __name__=='__main__':
    raise SystemExit(main())
