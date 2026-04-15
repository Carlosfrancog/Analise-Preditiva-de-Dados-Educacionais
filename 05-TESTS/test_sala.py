#!/usr/bin/env python3
"""Teste das funções de sala"""
import cads

try:
    # Testa adicionar_sala
    cads.adicionar_sala('Teste Turma 10', '10T')
    print('✅ Sala criada com sucesso!')
    
    # Verifica se foi criada
    salas = cads.get_salas()
    sala_teste = [s for s in salas if s['codigo'] == '10T']
    if sala_teste:
        print(f'✅ Sala encontrada: {sala_teste[0]["nome"]} ({sala_teste[0]["codigo"]})')
        
        # Testa remover_sala
        sala_id = sala_teste[0]['id']
        cads.remover_sala(sala_id)
        print('✅ Sala removida com sucesso!')
    else:
        print('❌ Sala não encontrada after create')
except Exception as e:
    print(f'❌ Erro: {e}')
