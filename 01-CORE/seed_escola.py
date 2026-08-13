#!/usr/bin/env python3
"""
seed_escola.py — Popula o banco com dados realistas de uma escola completa.
Uso: python seed_escola.py [--limpar]
"""
import sys, os, random, argparse
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "01-CORE"))
import cads

random.seed(42)

# ─── TURMAS ───────────────────────────────────────────────────────────────────
TURMAS = [
    ("6º Fundamental A", "6FA", "fundamental"),
    ("6º Fundamental B", "6FB", "fundamental"),
    ("7º Fundamental A", "7FA", "fundamental"),
    ("7º Fundamental B", "7FB", "fundamental"),
    ("8º Fundamental A", "8FA", "fundamental"),
    ("8º Fundamental B", "8FB", "fundamental"),
    ("9º Fundamental A", "9FA", "fundamental"),
    ("9º Fundamental B", "9FB", "fundamental"),
    ("1º Médio A",       "1MA", "medio"),
    ("1º Médio B",       "1MB", "medio"),
    ("2º Médio A",       "2MA", "medio"),
    ("2º Médio B",       "2MB", "medio"),
    ("3º Médio A",       "3MA", "medio"),
    ("3º Médio B",       "3MB", "medio"),
]

# ─── MATÉRIAS ─────────────────────────────────────────────────────────────────
MATERIAS_FUNDAMENTAL = [
    "Português", "Matemática", "Inglês", "Educação Física",
    "Arte", "História", "Geografia", "Ciências",
]
MATERIAS_MEDIO = [
    "Português", "Matemática", "Inglês", "Educação Física",
    "Arte", "História", "Geografia",
    "Física", "Química", "Biologia", "Filosofia", "Sociologia",
]

# Dificuldade relativa: negativo = mais difícil
DIFICULDADE = {
    "Matemática": -0.9, "Física": -1.1, "Química": -1.0,
    "Inglês": -0.5, "Ciências": -0.4, "Biologia": -0.5,
    "Português": -0.2, "História": -0.1, "Geografia": -0.1,
    "Filosofia": 0.1, "Sociologia": 0.2,
    "Arte": 0.6, "Educação Física": 1.2,
}

# ─── NOMES ────────────────────────────────────────────────────────────────────
MASCULINOS = [
    "João","Pedro","Lucas","Gabriel","Matheus","Rafael","Gustavo","Bruno",
    "Felipe","Rodrigo","Eduardo","André","Carlos","Diego","Fernando","Henrique",
    "Leonardo","Marcos","Paulo","Ricardo","Thiago","Victor","Alexandre","Daniel",
    "Luiz","Miguel","Nicolas","Otávio","Patrick","Renato","Samuel","Arthur",
    "Bernardo","Caio","Davi","Enzo","Felipe","Guilherme","Hugo","Igor",
]
FEMININOS = [
    "Maria","Ana","Júlia","Beatriz","Carla","Daniela","Elena","Fernanda",
    "Gabriela","Helena","Isabela","Juliana","Karen","Laura","Marina","Natalia",
    "Olivia","Patricia","Raquel","Sabrina","Tatiane","Vanessa","Aline","Bruna",
    "Camila","Diana","Elisa","Flavia","Giovanna","Heloisa","Iris","Jessica",
    "Larissa","Mariana","Nathalia","Paula","Renata","Sofia","Thaís","Vitória",
]
SOBRENOMES = [
    "Silva","Santos","Oliveira","Souza","Lima","Pereira","Ferreira","Costa",
    "Rodrigues","Almeida","Nascimento","Carvalho","Freitas","Gomes","Martins",
    "Araújo","Melo","Barbosa","Ribeiro","Cardoso","Rocha","Correia","Dias",
    "Nunes","Mendes","Moreira","Lopes","Teixeira","Andrade","Pinto","Ramos",
    "Cunha","Tavares","Castro","Campos","Guimarães","Marques","Cavalcanti","Borges",
]

ALUNOS_MIN, ALUNOS_MAX = 28, 37


def nome_aleatorio():
    if random.random() < 0.5:
        return f"{random.choice(MASCULINOS)} {random.choice(SOBRENOMES)}"
    return f"{random.choice(FEMININOS)} {random.choice(SOBRENOMES)}"


def perfil_aluno():
    """Retorna base_score e variância do perfil de desempenho do aluno."""
    r = random.random()
    if r < 0.22:        # em risco — ~22%
        return random.uniform(2.5, 4.9), random.uniform(0.5, 1.5)
    elif r < 0.52:      # médio-baixo — ~30%
        return random.uniform(5.0, 6.4), random.uniform(0.4, 1.2)
    elif r < 0.82:      # médio-alto — ~30%
        return random.uniform(6.5, 8.0), random.uniform(0.3, 1.0)
    else:               # destaque — ~18%
        return random.uniform(8.1, 9.6), random.uniform(0.2, 0.6)


def gerar_nota(base, dificuldade, bimestre_idx):
    """Gera uma nota para um bimestre específico, com tendência temporal."""
    trend = (bimestre_idx - 1.5) * random.gauss(0, 0.3)
    nota = base + dificuldade + trend + random.gauss(0, 0.8)
    return round(max(0.0, min(10.0, nota)), 1)


def seed(limpar=False):
    cads.init_db()
    conn = cads.get_conn()

    if limpar:
        conn.execute("DELETE FROM ml_features")
        conn.execute("DELETE FROM atividades")
        conn.execute("DELETE FROM presencas")
        conn.execute("DELETE FROM notas")
        conn.execute("DELETE FROM alunos")
        conn.execute("DELETE FROM materias")
        conn.execute("DELETE FROM salas")
        conn.commit()
        print("[Seed] Banco limpo.")

    # ── 1. Matérias ──────────────────────────────────────────────────────────
    todas_materias = list(dict.fromkeys(MATERIAS_FUNDAMENTAL + MATERIAS_MEDIO))
    materia_ids = {}
    for nome in todas_materias:
        existing = conn.execute("SELECT id FROM materias WHERE nome=?", (nome,)).fetchone()
        if existing:
            materia_ids[nome] = existing["id"]
        else:
            conn.execute("INSERT INTO materias (nome) VALUES (?)", (nome,))
            materia_ids[nome] = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.commit()
    print(f"[Seed] {len(materia_ids)} matérias.")

    # ── 2. Salas ─────────────────────────────────────────────────────────────
    sala_ids = {}
    for nome, codigo, tipo in TURMAS:
        existing = conn.execute("SELECT id FROM salas WHERE codigo=?", (codigo,)).fetchone()
        if existing:
            sala_ids[codigo] = (existing["id"], tipo)
        else:
            conn.execute("INSERT INTO salas (nome, codigo) VALUES (?,?)", (nome, codigo))
            sid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            sala_ids[codigo] = (sid, tipo)
    conn.commit()
    print(f"[Seed] {len(sala_ids)} salas.")

    # ── 3. Alunos + Notas ────────────────────────────────────────────────────
    total_alunos = 0
    total_notas  = 0

    for codigo, (sala_id, tipo) in sala_ids.items():
        n_alunos = random.randint(ALUNOS_MIN, ALUNOS_MAX)
        materias_sala = MATERIAS_MEDIO if tipo == "medio" else MATERIAS_FUNDAMENTAL
        aluno_seq = 1

        for _ in range(n_alunos):
            nome = nome_aleatorio()
            matricula = f"{codigo}{aluno_seq:04d}"
            aluno_seq += 1
            conn.execute(
                "INSERT INTO alunos (nome, sala_id, matricula) VALUES (?,?,?)",
                (nome, sala_id, matricula),
            )
            aluno_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            total_alunos += 1

            base, sigma = perfil_aluno()

            for materia in materias_sala:
                diff = DIFICULDADE.get(materia, 0)
                mat_id = materia_ids[materia]

                # N4 pode estar em branco para ~30% dos alunos (ano em aberto)
                has_n4 = random.random() > 0.30
                notas = [gerar_nota(base, diff, i) for i in range(4 if has_n4 else 3)]

                n1 = notas[0] if len(notas) > 0 else None
                n2 = notas[1] if len(notas) > 1 else None
                n3 = notas[2] if len(notas) > 2 else None
                n4 = notas[3] if len(notas) > 3 else None

                conn.execute(
                    "INSERT OR REPLACE INTO notas (aluno_id, materia_id, n1, n2, n3, n4) VALUES (?,?,?,?,?,?)",
                    (aluno_id, mat_id, n1, n2, n3, n4),
                )
                total_notas += 1

        conn.commit()
        print(f"  {codigo}: {n_alunos} alunos · {len(materias_sala)} matérias")

    conn.close()
    print(f"\n[Seed] Concluído: {total_alunos} alunos, {total_notas} registros de nota.")
    print("[Seed] Agora execute o treinamento em Configurações > Retreinar Modelos.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed do banco EduNotas")
    parser.add_argument("--limpar", action="store_true", help="Limpar dados existentes antes de inserir")
    args = parser.parse_args()
    seed(limpar=args.limpar)
