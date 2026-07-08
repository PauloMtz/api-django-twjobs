# twjobs-api

Agora nesta etapa a API evolui a listagem de `jobs` com filtros mais flexiveis, permitindo consultas mais proximas de um fluxo real de busca de vagas.

O projeto ja contava com detalhe, atualizacao, inativacao logica, paginacao e validacoes. Neste proximo commit, o foco passa a ser melhorar a experiencia de busca da listagem, com combinacao de filtros por texto, faixa salarial, senioridade, tipo de contratacao e habilidades.

## O que foi alterado neste commit

As principais alteracoes desta etapa foram:

- criacao do arquivo `jobs/filters.py` com o `JobFilterSet`
- adicao de filtros para `title` e `location` com busca parcial usando `icontains`
- adicao de filtros exatos para `job_type` e `job_level`
- adicao de filtros de faixa salarial com `salary_gte` e `salary_lte`
- adicao de filtro por habilidades via parametro `skills`, permitindo informar multiplos nomes separados por virgula
- integracao do `JobFilterSet` dentro da view `JobList`
- inclusao do app `django_filters` em `INSTALLED_APPS`
- organizacao da listagem para combinar filtros com a regra que continua exibindo apenas vagas ativas

Arquivos centrais desta entrega:

- `jobs/filters.py`
- `jobs/views.py`
- `setup/settings.py`

## Stack usada ate o momento

- Python 3.14 no ambiente atual
- Django 6.0.6
- djangorestframework
- django-filter
- python-decouple 3.8
- dj-database-url 3.1.2
- mysqlclient 2.2.8
- black 26.5.1

## Como executar o projeto

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
pip install djangorestframework
pip install django-filter
pip install python-decouple
pip install dj-database-url
pip install mysqlclient
pip install black
```

Observacao: o projeto esta preparado para usar SQLite por padrao. O `mysqlclient` so e necessario quando `ENV_DATABASE_URL` apontar para MySQL.

### 3. Configurar variaveis de ambiente

Copie o arquivo `.env.example` para `.env` e preencha os valores reais.

```cmd
copy .env.example .env
```

Exemplo para desenvolvimento com SQLite:

```env
ENV_SECRET_KEY=sua-chave-secreta
ENV_DEBUG=True
ENV_ALLOWED_HOSTS=127.0.0.1,localhost
ENV_DATABASE_URL=sqlite:///db.sqlite3
```

### 4. Aplicar migracoes

```cmd
python manage.py makemigrations
python manage.py migrate
```

### 5. Rodar o servidor

```cmd
python manage.py runserver
```

## Endpoints disponiveis

O projeto possui dois grupos principais de endpoints: `skills` e `jobs`.

### Base de skills

```text
/api/skills/
```

### 1. GET /api/skills/

Lista todas as habilidades cadastradas.

Exemplo de resposta:

```json
[
    {
        "id": 1,
        "name": "Python"
    },
    {
        "id": 2,
        "name": "Django"
    }
]
```

### 2. POST /api/skills/

Cria uma nova habilidade.

Corpo esperado:

```json
{
    "name": "Python"
}
```

### 3. GET /api/skills/<id>

Retorna uma habilidade especifica.

### 4. PUT /api/skills/<id>

Atualiza uma habilidade existente.

Corpo esperado:

```json
{
    "name": "Python e Django"
}
```

### 5. DELETE /api/skills/<id>

Remove uma habilidade existente com exclusao fisica.

### Base de jobs

```text
/api/jobs/
```

### 6. GET /api/jobs/

Lista as vagas ativas com paginacao e filtros.

Implementacao atual:

- busca inicialmente apenas registros com `is_active=True`
- aplica os filtros declarados em `JobFilterSet`
- pagina o resultado com `TWJobsPagination`
- devolve a resposta no formato padrao do DRF com `count`, `next`, `previous` e `results`

Filtros disponiveis na listagem:

- `title`: busca parcial no titulo
- `location`: busca parcial na localizacao
- `job_type`: filtro exato pelo tipo de vaga
- `job_level`: filtro exato pelo nivel
- `salary_gte`: salario minimo
- `salary_lte`: salario maximo
- `skills`: nomes de habilidades separados por virgula

Exemplos de consulta:

- `/api/jobs/?title=django`
- `/api/jobs/?location=remoto`
- `/api/jobs/?job_type=FULL_TIME&job_level=SENIOR`
- `/api/jobs/?salary_gte=3000&salary_lte=7000`
- `/api/jobs/?skills=Python,Django`
- `/api/jobs/?title=python&location=brasil&salary_gte=4000`

Exemplo de resposta:

```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Desenvolvedor Django Pleno",
            "description": "Atuar na evolucao da API de vagas",
            "company": "TreinaWeb",
            "location": "Remoto no Brasil",
            "job_type": "FULL_TIME",
            "job_level": "MIDDLE",
            "salary": 4500.0,
            "skills": [1, 2]
        },
        {
            "id": 2,
            "title": "Pessoa Desenvolvedora Backend Python",
            "description": "Implementar e manter servicos internos",
            "company": "Empresa X",
            "location": "Sao Paulo - SP",
            "job_type": "FULL_TIME",
            "job_level": "JUNIOR",
            "salary": 3500.0,
            "skills": [1]
        }
    ]
}
```

Observacoes:

- o campo `salary` continua sendo retornado como numero por causa de `COERCE_DECIMAL_TO_STRING = False`
- por padrao a pagina usa `PAGE_SIZE = 10`
- o cliente pode enviar `?size=20` para alterar o tamanho da pagina
- o tamanho maximo permitido por requisicao e `100`
- os filtros podem ser combinados na mesma requisicao

### 7. POST /api/jobs/

Cria uma nova vaga.

Corpo esperado:

```json
{
    "title": "Desenvolvedor Django Pleno",
    "description": "Atuar na evolucao da API de vagas",
    "company": "TreinaWeb",
    "location": "Remoto no Brasil",
    "job_type": "FULL_TIME",
    "job_level": "MIDDLE",
    "salary": 4500.00,
    "skills": [1, 2]
}
```

Validacoes relevantes do serializer:

- `title` com no minimo `10` caracteres
- `description` entre `10` e `150` caracteres
- `company` com no minimo `3` caracteres
- `location` com no minimo `10` caracteres
- `salary` com valor minimo de `1000`

Exemplo de resposta:

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
    "skills": [1, 2]
}
```

Observacao: o campo interno `is_active` existe no model, mas nao aparece na API porque foi excluido do serializer.

### 8. GET /api/jobs/<id>

Retorna uma vaga ativa especifica.

Implementacao atual:

- busca com `get_object_or_404(Job, pk=pk, is_active=True)`
- impede a exposicao de vagas inativas
- serializa o recurso com `JobSerializer(job)`

Exemplo de resposta:

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
    "skills": [1, 2]
}
```

### 9. PUT /api/jobs/<id>

Atualiza uma vaga ativa existente.

Corpo esperado:

```json
{
    "title": "Desenvolvedor Django Senior",
    "description": "Atuar na evolucao e manutencao da API",
    "company": "TreinaWeb",
    "location": "Remoto no Brasil",
    "job_type": "FULL_TIME",
    "job_level": "SENIOR",
    "salary": 6500.00,
    "skills": [1, 2]
}
```

Implementacao atual:

- reaproveita a mesma busca restrita a vagas ativas
- reutiliza `JobSerializer(job, data=request.data)`
- valida e persiste os dados atualizados

### 10. DELETE /api/jobs/<id>

Inativa uma vaga existente.

Implementacao atual:

- busca apenas vagas ainda ativas
- altera `is_active` para `False`
- salva a alteracao e retorna `204 No Content`

Na pratica, a vaga deixa de aparecer na listagem e no detalhe, mas o registro continua armazenado no banco.

## Exemplo de uso com curl

Listar skills:

```bash
curl http://127.0.0.1:8000/api/skills/
```

Buscar uma skill por id:

```bash
curl http://127.0.0.1:8000/api/skills/1
```

Atualizar uma skill:

```bash
curl -X PUT http://127.0.0.1:8000/api/skills/1 \
    -H "Content-Type: application/json" \
    -d '{"name":"Python e Django"}'
```

Remover uma skill:

```bash
curl -X DELETE http://127.0.0.1:8000/api/skills/1
```

Listar jobs com paginacao padrao:

```bash
curl http://127.0.0.1:8000/api/jobs/
```

Listar jobs com tamanho de pagina customizado:

```bash
curl "http://127.0.0.1:8000/api/jobs/?size=5"
```

Filtrar jobs por titulo:

```bash
curl "http://127.0.0.1:8000/api/jobs/?title=django"
```

Filtrar jobs por localizacao:

```bash
curl "http://127.0.0.1:8000/api/jobs/?location=remoto"
```

Filtrar jobs por tipo e nivel:

```bash
curl "http://127.0.0.1:8000/api/jobs/?job_type=FULL_TIME&job_level=SENIOR"
```

Filtrar jobs por faixa salarial:

```bash
curl "http://127.0.0.1:8000/api/jobs/?salary_gte=3000&salary_lte=7000"
```

Filtrar jobs por habilidades:

```bash
curl "http://127.0.0.1:8000/api/jobs/?skills=Python,Django"
```

Buscar uma job por id:

```bash
curl http://127.0.0.1:8000/api/jobs/1
```

Criar job:

```bash
curl -X POST http://127.0.0.1:8000/api/jobs/ \
    -H "Content-Type: application/json" \
    -d '{"title":"Desenvolvedor Django Pleno","description":"Atuar na evolucao da API de vagas","company":"TreinaWeb","location":"Remoto no Brasil","job_type":"FULL_TIME","job_level":"MIDDLE","salary":4500.00,"skills":[1,2]}'
```

Atualizar job:

```bash
curl -X PUT http://127.0.0.1:8000/api/jobs/1 \
    -H "Content-Type: application/json" \
    -d '{"title":"Desenvolvedor Django Senior","description":"Atuar na evolucao e manutencao da API","company":"TreinaWeb","location":"Remoto no Brasil","job_type":"FULL_TIME","job_level":"SENIOR","salary":6500.00,"skills":[1,2]}'
```

Inativar job:

```bash
curl -X DELETE http://127.0.0.1:8000/api/jobs/1
```

## O que melhora com esta etapa

Com este commit, a API de vagas passa a oferecer uma busca mais util sem exigir novas rotas ou regras especificas para cada consulta. As principais melhorias sao:

- a listagem de `jobs` fica mais flexivel para consumo por frontends, dashboards e clientes HTTP
- filtros podem ser combinados na mesma chamada, reduzindo processamento manual do lado cliente
- a busca por faixa salarial melhora consultas orientadas por expectativa de renda
- a busca por habilidades aproxima a API de um fluxo mais real de recrutamento
- a organizacao em `JobFilterSet` deixa a regra de filtragem mais clara e mais facil de evoluir

Na pratica, o projeto passa a ter uma API de vagas mais preparada para cenarios de pesquisa, navegacao e refinamento de resultados.

## Estado atual da aplicacao

Neste sexto commit:

- `skills` possui endpoints de lista, criacao, detalhe, atualizacao e remocao
- `jobs` possui endpoints de lista, criacao, detalhe, atualizacao e inativacao
- apenas vagas ativas aparecem na listagem e no detalhe
- a listagem de `jobs` e paginada
- o tamanho da pagina pode ser configurado por query string com `size`
- a listagem de `jobs` aceita filtros por titulo, localizacao, tipo, nivel, faixa salarial e habilidades
- o `JobSerializer` aplica validacoes minimas para campos importantes do dominio
- o campo `salary` continua sendo serializado como numero no JSON
