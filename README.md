# twjobs-api

Quarto commit da aplicacao: nesta etapa a API deixa de expor apenas a listagem e criacao de `skills` e passa a oferecer operacoes de detalhe para habilidades, alem de publicar a primeira versao da API de `jobs` com Django Rest Framework.

O foco agora e ampliar a estrutura iniciada no commit anterior, reaproveitando `APIView`, `ModelSerializer` e `Response` para cobrir novos fluxos da aplicacao e expor o relacionamento entre vagas e habilidades.

## O que foi alterado neste commit

As principais alteracoes desta etapa foram:

- criacao da view `SkillDetail` para consultar, atualizar e remover uma habilidade
- adicao da rota detalhada `api/skills/<pk>`
- uso de `get_object_or_404` para tratamento padronizado de registros inexistentes em `skills`
- criacao da view `JobList` para listar e criar vagas
- criacao do `JobSerializer` com `ModelSerializer`
- exposicao da rota `api/jobs/`
- serializacao do relacionamento many-to-many entre `jobs` e `skills`
- exclusao do campo interno `is_active` da resposta da API de vagas
- configuracao do DRF para manter campos `Decimal` como numero no JSON com `COERCE_DECIMAL_TO_STRING = False`

Arquivos centrais desta entrega:

- `skills/views.py`
- `skills/urls.py`
- `jobs/views.py`
- `jobs/serializers.py`
- `jobs/urls.py`
- `jobs/models.py`
- `setup/urls.py`
- `setup/settings.py`

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

O projeto agora possui dois grupos principais de endpoints: `skills` e `jobs`.

### Base de skills

```text
/api/skills/
```

### 1. GET /api/skills/

Lista todas as habilidades cadastradas.

Implementacao atual:

- busca os registros com `Skill.objects.all()`
- serializa a collection com `SkillSerializer(skills, many=True)`
- retorna os dados com `Response(serializer.data)`

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

Implementacao atual:

- recebe os dados com `request.data`
- cria o serializer com `SkillSerializer(data=request.data)`
- valida a entrada com `serializer.is_valid(raise_exception=True)`
- persiste o registro com `serializer.save()`
- retorna a skill criada com status `201 Created`

### 3. GET /api/skills/<id>

Retorna uma habilidade especifica.

Implementacao atual:

- busca o registro com `get_object_or_404(Skill, pk=pk)`
- serializa a instancia com `SkillSerializer(skill)`
- retorna os dados com `Response(serializer.data)`

Exemplo de resposta:

```json
{
    "id": 1,
    "name": "Python"
}
```

### 4. PUT /api/skills/<id>

Atualiza uma habilidade existente.

Corpo esperado:

```json
{
    "name": "Python e Django"
}
```

Implementacao atual:

- busca a skill pelo `pk`
- reaproveita `SkillSerializer(skill, data=request.data)`
- valida os dados com `raise_exception=True`
- salva e devolve o objeto atualizado

### 5. DELETE /api/skills/<id>

Remove uma habilidade existente.

Implementacao atual:

- busca a skill pelo `pk`
- executa `delete()`
- retorna status `204 No Content`

### Base de jobs

```text
/api/jobs/
```

### 6. GET /api/jobs/

Lista todas as vagas cadastradas.

Implementacao atual:

- busca os registros com `Job.objects.all()`
- serializa a collection com `JobSerializer(jobs, many=True)`
- retorna os dados com `Response(serializer.data)`

Exemplo de resposta:

```json
[
    {
        "id": 1,
        "title": "Desenvolvedor Django",
        "description": "Atuar na evolucao da API",
        "company": "TreinaWeb",
        "location": "Remoto",
        "job_type": "FULL_TIME",
        "job_level": "JUNIOR",
        "salary": 3500.0,
        "skills": [1, 2]
    }
]
```

Observacao: o campo `salary` e retornado como numero porque o projeto definiu `COERCE_DECIMAL_TO_STRING = False` no DRF.

### 7. POST /api/jobs/

Cria uma nova vaga.

Corpo esperado:

```json
{
    "title": "Desenvolvedor Django",
    "description": "Atuar na evolucao da API",
    "company": "TreinaWeb",
    "location": "Remoto",
    "job_type": "FULL_TIME",
    "job_level": "JUNIOR",
    "salary": 3500.00,
    "skills": [1, 2]
}
```

Implementacao atual:

- recebe os dados com `request.data`
- cria o serializer com `JobSerializer(data=request.data, context={"request": request})`
- valida a entrada com `serializer.is_valid(raise_exception=True)`
- persiste a vaga com `serializer.save()`
- retorna o recurso criado com status `201 Created`

Exemplo de resposta:

```json
{
    "id": 1,
    "title": "Desenvolvedor Django",
    "description": "Atuar na evolucao da API",
    "company": "TreinaWeb",
    "location": "Remoto",
    "job_type": "FULL_TIME",
    "job_level": "JUNIOR",
    "salary": 3500.0,
    "skills": [1, 2]
}
```

Observacao: o campo `is_active` existe no model, mas nao aparece na API porque foi excluido do serializer.

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

Listar jobs:

```bash
curl http://127.0.0.1:8000/api/jobs/
```

Criar job:

```bash
curl -X POST http://127.0.0.1:8000/api/jobs/ \
    -H "Content-Type: application/json" \
    -d '{"title":"Desenvolvedor Django","description":"Atuar na evolucao da API","company":"TreinaWeb","location":"Remoto","job_type":"FULL_TIME","job_level":"JUNIOR","salary":3500.00,"skills":[1,2]}'
```

## O que melhora com esta etapa

Com este commit, a API passa a cobrir mais casos reais da aplicacao. As principais melhorias sao:

- `skills` agora possui ciclo basico de leitura, atualizacao e remocao por identificador
- `jobs` passa a ser exposto por HTTP usando a mesma base do DRF adotada no commit anterior
- o relacionamento entre vagas e habilidades ja pode ser enviado e retornado pela API
- a aplicacao reduz tratamento manual de erros ao usar `get_object_or_404` e validacao padronizada do serializer
- a resposta da API fica mais alinhada ao dominio da aplicacao, com campos numericos e relacionamentos prontos para consumo

Na pratica, o projeto deixa de ter uma API restrita a `skills` e passa a expor uma base inicial para o fluxo de vagas.

## Estado atual da aplicacao

Neste quarto commit:

- `skills` possui endpoints de lista, criacao, detalhe, atualizacao e remocao
- `jobs` possui endpoints de lista e criacao
- a API continua baseada em Django Rest Framework
- o campo `salary` e serializado como numero no JSON
- o relacionamento many-to-many entre `jobs` e `skills` ja esta disponivel na API
- ainda nao existe endpoint de detalhe para `jobs`
