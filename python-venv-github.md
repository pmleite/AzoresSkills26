# Inicializar um projeto Python com venv e sincronizar com o GitHub

A ideia central é simples: o ambiente virtual fica **só na tua máquina** e nunca vai para o GitHub; o que se sincroniza é o código e a lista de dependências (`requirements.txt`), a partir da qual qualquer pessoa recria o venv.

## 1. Criar o projeto e o ambiente virtual

```bash
mkdir meu-projeto
cd meu-projeto
python3 -m venv .venv
```

Ativar o ambiente:

```bash
# Linux / macOS
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

Com o ambiente ativo, instalas o que precisas e registas as dependências:

```bash
pip install --upgrade pip
pip install requests        # exemplo
pip freeze > requirements.txt
```

## 2. Criar o `.gitignore`

Este é o passo que muita gente esquece. Cria um ficheiro `.gitignore` na raiz com, pelo menos:

```
.venv/
__pycache__/
*.pyc
.env
```

O `.env` é importante se guardares chaves ou palavras-passe em variáveis de ambiente.

## 3. Inicializar o Git e fazer o primeiro commit

```bash
git init
git add .
git commit -m "Commit inicial"
git branch -M main
```

## 4. Ligar ao GitHub

### Opção A – pela interface web

Cria um repositório vazio no GitHub (sem README nem .gitignore, para evitar conflitos) e depois:

```bash
git remote add origin https://github.com/UTILIZADOR/meu-projeto.git
git push -u origin main
```

### Opção B – com a GitHub CLI (`gh`)

Cria o repositório e faz o push de uma vez:

```bash
gh auth login        # só da primeira vez
gh repo create meu-projeto --private --source=. --push
```

O `-u` / `--push` deixa o ramo local associado ao remoto, por isso a partir daí basta `git push` e `git pull`.

## 5. Trabalhar noutra máquina (ou um colega)

```bash
git clone https://github.com/UTILIZADOR/meu-projeto.git
cd meu-projeto
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Notas práticas

- Sempre que instalares um pacote novo, atualiza o `requirements.txt` com `pip freeze > requirements.txt` antes do commit, senão o repositório fica dessincronizado do teu ambiente.
- Para autenticação no push, o GitHub já não aceita palavra-passe por HTTPS: usa um *personal access token*, chaves SSH, ou simplesmente o `gh auth login`, que trata disso por ti.
- Se o projeto crescer, vale a pena olhar para ferramentas como o `uv` ou o Poetry, que gerem venv e dependências de forma mais rigorosa (com ficheiros de lock). Para começar, o fluxo acima é o padrão e funciona bem.
