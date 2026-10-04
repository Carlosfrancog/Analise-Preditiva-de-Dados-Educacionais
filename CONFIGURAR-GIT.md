# Configuração do Git no Windows

Após extrair este projeto em `D:\EPA`, abrir o PowerShell e executar:

```powershell
Set-Location D:\EPA

git init
git branch -M main

git config user.name "Carlos Eduardo Franco Gabriel"
git config user.email "SEU_EMAIL_DO_GITHUB"

git remote add origin "https://github.com/Carlosfrancog/Analise-Preditiva-de-Dados-Educacionais.git"
git remote -v
git status
```

## Primeiro commit local

```powershell
git add .
git commit -m "feat: adiciona pipeline experimental do EduPredict"
```

## Conferir o GitHub antes de enviar

```powershell
git fetch origin
git log --oneline --decorate --all -10
```

Se o repositório remoto já possuir commits diferentes, não executar `push`
imediatamente. Primeiro integrar e revisar:

```powershell
git pull origin main --allow-unrelated-histories --no-rebase
```

Após resolver eventuais conflitos:

```powershell
git add .
git commit -m "chore: resolve integração com origin/main"
git push -u origin main
```

Se o repositório remoto estiver vazio, o envio será direto:

```powershell
git push -u origin main
```

O comando `git push --force` não faz parte deste procedimento.

