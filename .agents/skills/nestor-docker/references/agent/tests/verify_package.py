#!/usr/bin/env python3
"""Checagem estática de integridade dos artefatos do pacote. Sem Docker necessário."""
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
required=['README.md','AGENT.md','identity.md','principles.md','capabilities.md',
 'policies/authorization.md','policies/safety.md','policies/evidence.md',
 'runbooks/diagnostic-triage.md','runbooks/validation-gates.md',
 'schemas/task-request.schema.json','schemas/inventory.schema.json',
 'schemas/change-plan.schema.json','schemas/execution-report.schema.json',
 'schemas/handoff.schema.json','tools/docker_inventory.py']
missing=[p for p in required if not (ROOT/p).is_file()]
assert not missing, f'Arquivos ausentes: {missing}'
for file in (ROOT/'schemas').glob('*.json'):
    d=json.loads(file.read_text(encoding='utf-8'))
    assert d['$schema'].endswith('2020-12/schema')
    assert d['type']=='object' and d.get('additionalProperties') is False
for doc in ROOT.rglob('*.md'):
    content=doc.read_text(encoding='utf-8')
    # Apenas os links relativos explícitos com formato markdown.
    for link in re.findall(r'\]\(([^)]+)\)', content):
        if link.startswith(('https://','http://','#')): continue
        assert (doc.parent/link).exists(),f'Link quebrado: {doc}: {link}'
assert 'Paridade visual' not in (ROOT/'AGENT.md').read_text(encoding='utf-8')
print(f'OK: {len(required)} artefatos obrigatórios; {len(list((ROOT/"schemas").glob("*.json")))} schemas; Markdown verificado')
