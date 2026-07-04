# twjobs-api

API em Django para gerenciamento de vagas (`jobs`) e habilidades (`skills`).

## Stack usada ate o momento

- Python 3.14 no ambiente atual
- Django 6.0.6
- python-decouple 3.8
- dj-database-url 3.1.2
- mysqlclient 2.2.8
- black 26.5.1

## Como criar o projeto do zero

### 1. Criar e ativar ambiente virtual

No Windows CMD:

```cmd
python -m venv .venv

.venv\Scripts\activate
```

### 2. Instalar dependencias

```cmd
python -m pip install --upgrade pip
pip install Django 
pip install python-decouple 
pip install dj-database-url 
pip install mysqlclient 
pip install black
```

Observacao: o projeto esta preparado para usar SQLite por padrao. O `mysqlclient` so e necessario quando a variavel `ENV_DATABASE_URL` apontar para MySQL.

### 3. Criar o projeto Django

Dentro da pasta do projeto twjobs

```cmd
django-admin startproject setup .
```

Esse comando cria a pasta `setup/` com os arquivos principais do projeto e o `manage.py` na raiz.

### 4. Criar os apps

```cmd
python manage.py startapp jobs
python manage.py startapp skills
```

Depois disso, os apps precisam ser adicionados em `INSTALLED_APPS` dentro de [setup/settings.py](/d:/paulo/py-workspace/curso-treinaweb/_django/twjobs-api/setup/settings.py).

## Configuracoes aplicadas ate o momento

As configuracoes atuais do projeto estao concentradas em [setup/settings.py](/d:/paulo/py-workspace/curso-treinaweb/_django/twjobs-api/setup/settings.py):

- Leitura de variaveis de ambiente com `python-decouple`
- Leitura da conexao com banco via `dj-database-url`
- `LANGUAGE_CODE = "pt-br"`
- `TIME_ZONE = "UTC"`
- Apps registrados: `jobs` e `skills`
- Banco padrao com fallback para SQLite em `db.sqlite3`

Trecho conceitual da configuracao atual:

```python
from decouple import Csv, config
from dj_database_url import parse as dburl

SECRET_KEY = config("ENV_SECRET_KEY")
DEBUG = config("ENV_DEBUG", cast=bool, default=False)
ALLOWED_HOSTS = config("ENV_ALLOWED_HOSTS", cast=Csv())

DATABASES = {
    "default": config(
        "ENV_DATABASE_URL",
        default="sqlite:///db.sqlite3",
        cast=dburl,
    ),
}
```

## Arquivo .env

O arquivo `.env` contem os valores reais usados localmente pela aplicacao. Ele nao deve ser versionado, porque normalmente guarda dados sensiveis, principalmente a chave secreta e possiveis credenciais de banco.

Variaveis usadas hoje:

- `ENV_SECRET_KEY`: chave secreta do Django
- `ENV_DEBUG`: ativa ou desativa modo debug
- `ENV_ALLOWED_HOSTS`: lista de hosts separada por virgula
- `ENV_DATABASE_URL`: URL de conexao com o banco

Exemplo de `.env` para desenvolvimento com SQLite:

```env
ENV_SECRET_KEY=sua-chave-secreta
ENV_DEBUG=True
ENV_ALLOWED_HOSTS=127.0.0.1,localhost
ENV_DATABASE_URL=sqlite:///db.sqlite3
```

Exemplo de `.env` para desenvolvimento com MySQL:

```env
ENV_SECRET_KEY=sua-chave-secreta
ENV_DEBUG=True
ENV_ALLOWED_HOSTS=127.0.0.1,localhost
ENV_DATABASE_URL=mysql://usuario:senha@localhost:3306/twjobs
```

## Arquivo .env.example

O arquivo [.env.example](/d:/paulo/py-workspace/curso-treinaweb/_django/twjobs-api/.env.example) e o arquivo falso do projeto. Ele serve como modelo para mostrar quais variaveis precisam existir no `.env`, sem expor segredos reais.

Fluxo recomendado:

1. Copiar `.env.example` para `.env`
2. Preencher os valores reais
3. Ajustar o banco que deseja usar

No CMD:

```cmd
copy .env.example .env
```

## Banco de dados e migracoes

Aplicar as migracoes:

```cmd
python manage.py makemigrations
python manage.py migrate
```

Rodar o servidor local:

```cmd
python manage.py runserver
```

## Estrutura atual dos apps

- `jobs`: contem o modelo `Job`, com relacionamento muitos-para-muitos com `skills.Skill`
- `skills`: contem o modelo `Skill`

## Arquivos importantes

- [manage.py](/d:/user/workspace/curso-django/twjobs-api/manage.py)
- [setup/settings.py](/d:/user/workspace/curso-django/twjobs-api/setup/settings.py)
- [jobs/models.py](/d:/user/workspace/curso-django/twjobs-api/jobs/models.py)
- [skills/models.py](/d:/user/workspace/curso-django/twjobs-api/skills/models.py)
- [.env.example](/d:/user/workspace/curso-django/twjobs-api/.env.example)