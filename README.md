# twjobs-api

API REST em Django para cadastro de habilidades e vagas. O projeto expõe endpoints para `skills` e `jobs`, com paginação, filtros, validações de domínio, inativação lógica de vagas e links HATEOAS nas respostas de `jobs`.

## Stack

- Python 3.14
- Django 6.0.6
- djangorestframework
- django-filter
- python-decouple
- dj-database-url
- mysqlclient

## Instalação

### 1. Criar e ativar o ambiente virtual

No Windows CMD:

```cmd
python -m venv .venv
.venv\Scripts\activate
```

### 2. Instalar as dependências

```cmd
python -m pip install --upgrade pip
pip install Django djangorestframework django-filter python-decouple dj-database-url mysqlclient
```

Observacao: o projeto usa SQLite por padrao. O `mysqlclient` so e necessario quando `ENV_DATABASE_URL` apontar para MySQL.

### 3. Configurar o ambiente

Crie o arquivo `.env` a partir de `.env.example`:

```cmd
copy .env.example .env
```

Exemplo de configuracao:

```env
ENV_SECRET_KEY=sua-chave-secreta
ENV_DEBUG=True
ENV_ALLOWED_HOSTS=127.0.0.1,localhost
ENV_DATABASE_URL=sqlite:///db.sqlite3
```

### 4. Aplicar as migracoes

```cmd
python manage.py makemigrations
python manage.py migrate
```

## Como rodar

Suba o servidor de desenvolvimento:

```cmd
python manage.py runserver
```

API disponivel em `http://127.0.0.1:8000/api/`.

## Endpoints

### Skills

- `GET /api/skills/`
- `POST /api/skills/`
- `GET /api/skills/<id>`
- `PUT /api/skills/<id>`
- `DELETE /api/skills/<id>`

### Jobs

- `GET /api/jobs/`
- `POST /api/jobs/`
- `GET /api/jobs/<id>`
- `PUT /api/jobs/<id>`
- `DELETE /api/jobs/<id>`

## Filtros de jobs

A listagem de vagas retorna apenas registros com `is_active=True` e aceita os filtros abaixo por query string:

- `title`: busca parcial por titulo
- `location`: busca parcial por localizacao
- `job_type`: filtro exato por tipo de vaga
- `job_level`: filtro exato por nivel
- `salary_gte`: salario minimo
- `salary_lte`: salario maximo
- `skills`: nomes de habilidades separados por virgula
- `size`: tamanho da pagina, com maximo de `100`

Exemplos:

```text
/api/jobs/?title=django
/api/jobs/?job_type=FULL_TIME&job_level=SENIOR
/api/jobs/?salary_gte=3000&salary_lte=7000
/api/jobs/?skills=Python,Django
```

## Exemplo de resposta com HATEOAS

As respostas de `jobs` incluem um campo `links` com as ações disponíveis para o recurso.

```json
{
    "id": 1,
    "title": "Desenvolvedor Django Pleno",
    "description": "Atuar na evolucao da API de vagas",
    "company": "TreinaWeb",
    "location": "Remoto no Brasil",
    "job_type": "FULL_TIME",
    "job_level": "MIDDLE",
    "salary": 4500.0,
    "skills": [1, 2],
    "links": [
        {
            "type": "GET",
            "rel": "self",
            "href": "http://127.0.0.1:8000/api/jobs/1"
        },
        {
            "type": "PUT",
            "rel": "update_job",
            "href": "http://127.0.0.1:8000/api/jobs/1"
        },
        {
            "type": "DELETE",
            "rel": "delete_job",
            "href": "http://127.0.0.1:8000/api/jobs/1"
        }
    ]
}
```

## Regras atuais

- `jobs` usa exclusao logica com `is_active=False`
- vagas inativas nao aparecem na listagem nem no detalhe
- a listagem de `jobs` e paginada
- `salary` e serializado como numero no JSON
- o `JobSerializer` valida campos como titulo, descricao, empresa, localizacao e salario minimo
