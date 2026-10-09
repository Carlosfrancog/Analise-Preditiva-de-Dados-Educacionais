#!/usr/bin/env python3
"""Gera schemas versionados de contrato (biblioteca padrão)."""
import json
from pathlib import Path

DIR = Path(__file__).resolve().parents[1] / 'schemas'
DRAFT = 'https://json-schema.org/draft/2020-12/schema'

def obj(props, required=(), *, additional=False):
    return {'type':'object','properties':props,'required':list(required),'additionalProperties':additional}

def arr(item):
    return {'type':'array','items':item}

def choice(*values):
    return {'type':'string','enum':list(values)}

EVIDENCE = obj({
    'label':choice('FACT','INFERENCE','HYPOTHESIS','UNKNOWN'),
    'statement':{'type':'string','minLength':1},
    'source':{'type':['string','null']},
    'collected_at':{'type':['string','null'],'format':'date-time'},
    'context':{'type':['string','null']},
    'confidence':choice('confirmed','probable','uncertain','not_assessed')
}, ('label','statement','confidence'))
TEST = obj({
    'name':{'type':'string','minLength':1},
    'status':choice('passed','failed','blocked','not_run','inconclusive'),
    'evidence':{'type':['string','null']},
    'reason':{'type':['string','null']}
},('name','status'))
RISK = obj({
    'description':{'type':'string','minLength':1},
    'severity':choice('low','medium','high','critical','unknown'),
    'mitigation':{'type':['string','null']}
},('description','severity'))

def write(name, title, desc, properties, required):
    data={'$schema':DRAFT,'$id':f'https://schemas.nestor.local/docker/1.0/{name}.schema.json',
          'title':title,'description':desc,**obj(properties,required)}
    (DIR/f'{name}.schema.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

write('task-request','Nestor Docker task request','Contrato de entrada, inclusive limites de operação',{
 'schema_version':{'const':'1.0'},
 'task_id':{'type':'string','minLength':1},
 'objective':{'type':'string','minLength':1},
 'environment':choice('dev','test','homolog','prod','unknown'),
 'docker_context':{'type':['string','null']},
 'repository_path':{'type':['string','null']},
 'project':{'type':['string','null']},
 'services':arr({'type':'string'}),
 'requested_mode':choice('inspect','edit_files','test_isolated','operate','critical'),
 'authorized_operations':arr({'type':'string'}),
 'constraints':arr({'type':'string'}),
 'acceptance_criteria':arr({'type':'string'})
},('schema_version','task_id','objective','environment','requested_mode','authorized_operations'))
write('inventory','Nestor Docker inventory','Estado inventariado com coleta permitida e natureza da evidência',{
 'schema_version':{'const':'1.0'},
 'environment':choice('dev','test','homolog','prod','unknown'),
 'collection_mode':choice('offline','live','hybrid'),
 'docker_context':{'type':['string','null']},
 'collected_at':{'type':['string','null'],'format':'date-time'},
 'engine_version':{'type':['string','null']},
 'compose_version':{'type':['string','null']},
 'services':arr(obj({'name':{'type':'string'},'state':{'type':['string','null']},'image':{'type':['string','null']},'health':{'type':['string','null']}} ,('name',))),
 'files':arr(obj({'path':{'type':'string'},'kind':{'type':'string'},'bytes':{'type':'integer','minimum':0}},('path','kind','bytes'))),
 'evidence':arr(EVIDENCE),
 'limitations':arr({'type':'string'})
},('schema_version','environment','collection_mode','services','files','evidence','limitations'))
write('change-plan','Nestor Docker change plan','Planejamento e gates antes de mutação',{
 'schema_version':{'const':'1.0'},
 'task_id':{'type':'string','minLength':1},
 'environment':choice('dev','test','homolog','prod','unknown'),
 'objective':{'type':'string','minLength':1},
 'risk_level':choice('L0','L1','L2','L3','L4'),
 'targets':arr({'type':'string'}),
 'changes':arr(obj({'action':{'type':'string'},'target':{'type':'string'},'reason':{'type':'string'},'approval_required':{'type':'boolean'}},('action','target','reason','approval_required'))),
 'authorization':obj({'status':choice('approved','required','denied','not_applicable'), 'reference':{'type':['string','null']}},('status',)),
 'data_impact':{'type':'string'},
 'service_impact':{'type':'string'},
 'preconditions':arr({'type':'string'}),
 'validation_steps':arr({'type':'string'}),
 'rollback_steps':arr({'type':'string'}),
 'risks':arr(RISK)
},('schema_version','task_id','environment','objective','risk_level','changes','authorization','data_impact','service_impact','validation_steps','rollback_steps'))
write('execution-report','Nestor Docker execution report','Resultado honesto e rastreável da execução',{
 'schema_version':{'const':'1.0'},
 'task_id':{'type':'string','minLength':1},
 'objective':{'type':'string','minLength':1},
 'environment':choice('dev','test','homolog','prod','unknown'),
 'docker_context':{'type':['string','null']},
 'status':choice('verified','partial','blocked','not_verified'),
 'diagnosis':{'type':'string'},
 'root_cause':{'type':['string','null']},
 'evidence':arr(EVIDENCE),
 'files_changed':arr({'type':'string'}),
 'operational_actions':arr({'type':'string'}),
 'impact':{'type':'string'},
 'persistence_security':{'type':'string'},
 'tests':arr(TEST),
 'risks':arr(RISK),
 'rollback':{'type':['string','null']},
 'pending':arr({'type':'string'}),
 'next_steps':arr({'type':'string'})
},('schema_version','task_id','objective','environment','status','diagnosis','evidence','files_changed','operational_actions','impact','persistence_security','tests','risks','pending','next_steps'))
write('handoff','Nestor inter-agent handoff','Informações mínimas entre agentes, sem secrets',{
 'schema_version':{'const':'1.0'},
 'task_id':{'type':'string','minLength':1},
 'from_agent':{'const':'Nestor Docker'},
 'to_agent':{'type':'string','minLength':1},
 'objective':{'type':'string'},
 'scope':{'type':'string'},
 'facts':arr(EVIDENCE),
 'requested_action':{'type':'string'},
 'constraints':arr({'type':'string'}),
 'artifacts':arr({'type':'string'}),
 'secrets_included':{'const':False}
},('schema_version','task_id','from_agent','to_agent','objective','scope','facts','requested_action','constraints','secrets_included'))
print(f'Generated {len(list(DIR.glob("*.schema.json")))} schemas')
