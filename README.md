# twjobs-api

Segundo commit da aplicacao: neste ponto o projeto deixa de ser apenas a estrutura inicial em Django e passa a expor os primeiros endpoints HTTP da API sem usar Django Rest Framework.

O foco desta etapa foi criar a base da API de `skills`, mantendo a implementacao manual com classes baseadas em `django.views.View`, serializacao simples e respostas em JSON.

## O que foi alterado neste commit

As principais alteracoes desta etapa foram:

- criacao da model `Skill` com o campo `name`
- criacao do metodo `to_json()` para transformar a model em dicionario
- criacao da view `SkillList` sem DRF
- criacao da rota `api/skills/`
- implementacao dos endpoints de listagem e criacao de skills
- uso de `csrf_exempt` para permitir requisicoes POST sem formulario HTML tradicional

Arquivos centrais desta entrega:

- `skills/models.py`
- `skills/views.py`
- `skills/urls.py`
- `setup/urls.py`

## Stack usada ate o momento

- Python 3.14 no ambiente atual
- Django 6.0.6
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

## Endpoints criados sem Django Rest Framework

Embora exista apenas uma URL registrada, esta rota expoe dois endpoints logicos por metodo HTTP.

Base URL:

```text
/api/skills/
```

### 1. GET /api/skills/

Lista todas as habilidades cadastradas.

Implementacao atual:

- busca todos os registros com `Skill.objects.all()`
- converte cada item com `to_json()`
- retorna um array JSON

Exemplo de resposta:

```json
[
    {
        "name": "Python"
    },
    {
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

- faz o parse manual do corpo com `json.loads(request.body)`
- le o campo `name`
- cria o registro com `Skill.objects.create(...)`
- retorna o JSON da skill criada com status `201 Created`

Exemplo de resposta:

```json
{
    "name": "Python"
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

## Limitacoes de nao utilizar Django Rest Framework

Nesta etapa a API foi criada manualmente para fins de aprendizado. Isso funciona para cenarios simples, mas traz limitacoes importantes:

- nao existe serializer dedicado para validar e transformar dados
- a validacao de entrada ainda e minima ou inexistente
- erros de JSON invalido, campo ausente ou valor vazio nao estao tratados
- a view precisa cuidar manualmente de parse, persistencia e resposta
- nao ha recursos nativos de paginacao, filtros, autenticacao e permissoes
- nao ha browsable API para inspecionar e testar endpoints pelo navegador
- o tratamento de codigos HTTP e mensagens de erro precisa ser feito manualmente
- a escalabilidade da manutencao piora conforme surgem mais endpoints

Na pratica, sem DRF a aplicacao exige mais codigo repetitivo e mais cuidado para manter padrao de resposta, validacao e seguranca.

## Estado atual da aplicacao

Neste segundo commit:

- a API de `skills` ja responde em JSON
- a criacao e a listagem estao funcionando sem DRF
- o app `jobs` ja possui model, mas ainda nao expoe endpoints HTTP
- a aplicacao ainda esta em uma fase inicial, com foco em estrutura e aprendizado do fluxo manual do Django