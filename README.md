# twjobs-api

Terceiro commit da aplicacao: nesta etapa o projeto deixa de expor a API de `skills` manualmente e passa a utilizar Django Rest Framework.

O foco agora e substituir o fluxo baseado em `json.loads`, dicionarios manuais e `JsonResponse` por componentes proprios do DRF, com serializer dedicado, `APIView` e respostas padronizadas com `Response`.

## O que foi alterado neste commit

As principais alteracoes desta etapa foram:

- instalacao do Django Rest Framework no projeto
- adicao de `rest_framework` em `INSTALLED_APPS`
- criacao do `SkillSerializer` com `ModelSerializer`
- refatoracao da view `SkillList` para herdar de `APIView`
- substituicao da serializacao manual por `serializer.data`
- uso de `request.data` no lugar do parse manual de JSON
- validacao da entrada com `serializer.is_valid(raise_exception=True)`
- remocao da necessidade de `csrf_exempt` na rota da API

Arquivos centrais desta entrega:

- `skills/serializers.py`
- `skills/views.py`
- `skills/urls.py`
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

## Endpoints criados com Django Rest Framework

Embora exista apenas uma URL registrada, esta rota expoe dois endpoints logicos por metodo HTTP.

Base URL:

```text
/api/skills/
```

### 1. GET /api/skills/

Lista todas as habilidades cadastradas.

Implementacao atual:

- busca todos os registros com `Skill.objects.all()`
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

Exemplo de resposta:

```json
{
    "id": 1,
    "name": "Python"
}
```

Exemplo de resposta quando a entrada e invalida:

```json
{
    "name": [
        "This field may not be blank."
    ]
}
```

## Exemplo de uso com curl

Listar skills:

```bash
curl http://127.0.0.1:8000/api/skills/
```

Criar skill:

```bash
curl -X POST http://127.0.0.1:8000/api/skills/ \
    -H "Content-Type: application/json" \
    -d '{"name":"Python"}'
```

## O que melhora com o Django Rest Framework

Nesta etapa a API continua simples, mas passa a usar uma base mais adequada para crescer. As principais vantagens sao:

- serializer dedicado para transformar e validar dados
- reducao do codigo manual na view
- tratamento padronizado de erros de validacao
- leitura de entrada via `request.data`, sem parse manual do corpo
- respostas HTTP mais consistentes com `Response`
- suporte nativo a browsable API do DRF
- base pronta para evoluir com autenticacao, permissoes, filtros e paginacao

Na pratica, o DRF reduz repeticao, melhora a manutencao e deixa a API mais preparada para novas funcionalidades.

## Estado atual da aplicacao

Neste terceiro commit:

- a API de `skills` continua respondendo em JSON
- a implementacao agora usa Django Rest Framework
- a listagem e a criacao passam por serializer e validacao do DRF
- a rota `api/skills/` continua ativa, mas com uma base mais robusta
- o app `jobs` ja possui model, mas ainda nao expoe endpoints HTTP
