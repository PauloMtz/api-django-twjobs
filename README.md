# twjobs-api

Agora nesta etapa a API evolui o fluxo de `jobs` com operacoes de detalhe, inativacao logica, paginacao e regras de validacao mais proximas do dominio.

O foco agora deixa de ser apenas expor vagas e passa a controlar melhor como elas sao consultadas, atualizadas e removidas da API, mantendo o historico no banco e melhorando a experiencia de consumo da listagem.

## O que foi alterado neste commit

As principais alteracoes desta etapa foram:

- criacao da view `JobDetail` para consultar, atualizar e inativar vagas individualmente
- adicao da rota detalhada `api/jobs/<pk>`
- filtro das consultas de vagas para retornar apenas registros com `is_active=True`
- substituicao da exclusao fisica por exclusao logica em `jobs`, marcando `is_active=False`
- reaproveitamento de `get_object_or_404` para manter o tratamento padronizado de vagas inexistentes ou inativas
- criacao da classe `TWJobsPagination` baseada em `PageNumberPagination`
- configuracao de paginacao global no DRF com `core.pagination.TWJobsPagination`
- liberacao de ajuste de tamanho da pagina com o parametro `size`
- definicao de limite maximo de `100` itens por pagina
- adicao de validacoes de negocio no `JobSerializer`

Arquivos centrais desta entrega:

- `jobs/views.py`
- `jobs/urls.py`
- `jobs/serializers.py`
- `core/pagination.py`
- `setup/settings.py`
- `setup/urls.py`

## Stack usada ate o momento

- Python 3.14 no ambiente atual
- Django 6.0.6
- djangorestframework
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

Lista as vagas ativas com paginacao.

Implementacao atual:

- busca apenas registros com `Job.objects.filter(is_active=True)`
- pagina o resultado com `TWJobsPagination`
- devolve a resposta no formato padrao do DRF com `count`, `next`, `previous` e `results`

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

Com este commit, a API de vagas passa a cobrir um fluxo bem mais completo. As principais melhorias sao:

- `jobs` agora possui endpoints de lista, criacao, detalhe, atualizacao e inativacao
- a exclusao logica preserva dados historicos sem manter a vaga visivel para consumo comum
- a listagem paginada reduz carga de resposta e prepara a API para volumes maiores
- o serializer passa a bloquear dados inconsistentes antes da persistencia
- a API deixa mais claro o comportamento de registros ativos e inativos

Na pratica, o projeto passa a ter uma API de vagas mais segura para evoluir e mais proxima de um fluxo real de publicacao e manutencao de oportunidades.

## Estado atual da aplicacao

Neste quinto commit:

- `skills` possui endpoints de lista, criacao, detalhe, atualizacao e remocao
- `jobs` possui endpoints de lista, criacao, detalhe, atualizacao e inativacao
- apenas vagas ativas aparecem na listagem e no detalhe
- a listagem de `jobs` e paginada
- o tamanho da pagina pode ser configurado por query string com `size`
- o `JobSerializer` aplica validacoes minimas para campos importantes do dominio
- o campo `salary` continua sendo serializado como numero no JSON
