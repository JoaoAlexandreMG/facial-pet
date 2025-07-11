# Documentação da API - Facial PET

Esta documentação descreve os endpoints da API do sistema Facial PET.

## Base URL

```
http://localhost:5000
```

## Autenticação

Atualmente, o sistema não requer autenticação. Para uso em produção, implemente autenticação adequada.

## Endpoints

### Eventos

#### Listar Eventos
```http
GET /
```

**Resposta:**
- `200 OK`: Página HTML com lista de eventos

#### Criar Evento
```http
POST /evento/novo
```

**Parâmetros do Form:**
- `nome` (string, obrigatório): Nome do evento
- `descricao` (string, opcional): Descrição do evento
- `data_inicio` (date, opcional): Data de início
- `data_fim` (date, opcional): Data de fim

**Resposta:**
- `302 Found`: Redirect para lista de eventos
- `400 Bad Request`: Dados inválidos

#### Visualizar Evento
```http
GET /evento/<int:evento_id>
```

**Parâmetros da URL:**
- `evento_id` (int): ID do evento

**Resposta:**
- `200 OK`: Página HTML com detalhes do evento
- `404 Not Found`: Evento não encontrado

#### Excluir Evento
```http
POST /evento/<int:evento_id>/excluir
```

**Parâmetros da URL:**
- `evento_id` (int): ID do evento

**Resposta:**
- `302 Found`: Redirect para lista de eventos
- `404 Not Found`: Evento não encontrado

### Momentos

#### Criar Momento
```http
POST /evento/<int:evento_id>/momento/novo
```

**Parâmetros da URL:**
- `evento_id` (int): ID do evento

**Parâmetros do Form:**
- `nome` (string, obrigatório): Nome do momento
- `data` (date, opcional): Data do momento
- `periodo` (string, opcional): Período (ex: manhã, tarde, noite)

**Resposta:**
- `302 Found`: Redirect para detalhes do evento
- `400 Bad Request`: Dados inválidos

#### Excluir Momento
```http
POST /momento/<int:moment_id>/excluir
```

**Parâmetros da URL:**
- `moment_id` (int): ID do momento

**Resposta:**
- `302 Found`: Redirect para detalhes do evento
- `404 Not Found`: Momento não encontrado

### Participantes

#### Criar Participante
```http
POST /evento/<int:evento_id>/participante/novo
```

**Parâmetros da URL:**
- `evento_id` (int): ID do evento (opcional)

**Parâmetros do Form:**
- `nome` (string, obrigatório): Nome do participante
- `imagem` (file, opcional): Arquivo de imagem
- `img_data_url` (string, opcional): Imagem em base64 (webcam)

**Resposta:**
- `302 Found`: Redirect conforme contexto
- `400 Bad Request`: Dados inválidos

#### Adicionar Participante ao Evento
```http
POST /evento/<int:evento_id>/participante/adicionar
```

**Parâmetros da URL:**
- `evento_id` (int): ID do evento

**Parâmetros do Form:**
- `participante_id` (int, obrigatório): ID do participante

**Resposta:**
- `302 Found`: Redirect para detalhes do evento
- `400 Bad Request`: Dados inválidos

#### Gerenciar Participantes
```http
GET /gerenciar
POST /gerenciar
```

**Parâmetros do Form (POST):**
- `excluir` (list): Lista de IDs para excluir

**Resposta:**
- `200 OK`: Página HTML de gerenciamento
- `302 Found`: Redirect após exclusão

### Presença

#### Marcar Presença
```http
POST /momento/<int:momento_id>/presenca
```

**Parâmetros da URL:**
- `momento_id` (int): ID do momento

**Parâmetros do Form:**
- `participante_id` (int, obrigatório): ID do participante

**Resposta:**
- `302 Found`: Redirect para página de presença
- `400 Bad Request`: Dados inválidos

#### Reconhecimento Facial
```http
POST /momento/<int:momento_id>/presenca/reconhecer
```

**Parâmetros da URL:**
- `momento_id` (int): ID do momento

**Parâmetros do Form:**
- `img_data_url` (string, obrigatório): Imagem em base64

**Resposta JSON:**
```json
{
  "success": true,
  "msg": "Presença registrada para João Silva",
  "participante_id": 123
}
```

ou

```json
{
  "success": false,
  "msg": "Pessoa não reconhecida"
}
```

### Reconhecimento

#### Reconhecer Pessoa
```http
POST /reconhecer
```

**Parâmetros do Form:**
- `img_data_url` (string, obrigatório): Imagem em base64

**Resposta JSON:**
```json
{
  "success": true,
  "nome": "João Silva"
}
```

ou

```json
{
  "success": false,
  "msg": "Pessoa não reconhecida"
}
```

### Utilitários

#### Obter Foto
```http
GET /foto/<string:nome>
```

**Parâmetros da URL:**
- `nome` (string): Nome do participante

**Resposta:**
- `200 OK`: Arquivo de imagem
- `404 Not Found`: Foto não encontrada

#### Buscar Participantes (AJAX)
```http
GET /buscar_participantes?q=<query>
```

**Parâmetros da Query:**
- `q` (string): Termo de busca

**Resposta JSON:**
```json
[
  {
    "id": 1,
    "nome": "João Silva"
  },
  {
    "id": 2,
    "nome": "Maria Santos"
  }
]
```

## Códigos de Status

- `200 OK`: Requisição bem-sucedida
- `302 Found`: Redirecionamento
- `400 Bad Request`: Dados inválidos
- `404 Not Found`: Recurso não encontrado
- `500 Internal Server Error`: Erro interno do servidor

## Tratamento de Erros

### Formato de Erro
```json
{
  "error": "Descrição do erro",
  "code": "ERROR_CODE"
}
```

### Tipos de Erro Comuns

- **INVALID_IMAGE**: Formato de imagem inválido
- **FACE_NOT_FOUND**: Nenhum rosto detectado na imagem
- **PARTICIPANT_NOT_FOUND**: Participante não encontrado
- **EVENT_NOT_FOUND**: Evento não encontrado
- **MOMENT_NOT_FOUND**: Momento não encontrado
- **ALREADY_PRESENT**: Participante já marcou presença

## Exemplos de Uso

### Criar um Evento com JavaScript

```javascript
const formData = new FormData();
formData.append('nome', 'Workshop Python');
formData.append('descricao', 'Workshop sobre desenvolvimento Python');
formData.append('data_inicio', '2025-07-15');

fetch('/evento/novo', {
    method: 'POST',
    body: formData
})
.then(response => {
    if (response.redirected) {
        window.location.href = response.url;
    }
});
```

### Reconhecimento Facial com JavaScript

```javascript
// Capturar imagem da webcam
const canvas = document.getElementById('canvas');
const video = document.getElementById('video');
canvas.getContext('2d').drawImage(video, 0, 0, 320, 240);
const dataUrl = canvas.toDataURL('image/jpeg');

// Enviar para reconhecimento
fetch('/reconhecer', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: 'img_data_url=' + encodeURIComponent(dataUrl)
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        console.log('Pessoa reconhecida:', data.nome);
    } else {
        console.log('Erro:', data.msg);
    }
});
```

### Buscar Participantes com Autocomplete

```javascript
function buscarParticipantes(query) {
    fetch(`/buscar_participantes?q=${encodeURIComponent(query)}`)
    .then(response => response.json())
    .then(participantes => {
        const lista = document.getElementById('autocomplete-list');
        lista.innerHTML = '';
        
        participantes.forEach(p => {
            const item = document.createElement('div');
            item.className = 'list-group-item list-group-item-action';
            item.textContent = p.nome;
            item.onclick = () => selecionarParticipante(p);
            lista.appendChild(item);
        });
        
        lista.style.display = 'block';
    });
}
```

## Limitações

- Máximo de 1 rosto por imagem para reconhecimento
- Formatos de imagem suportados: JPG, JPEG, PNG
- Tamanho máximo de imagem: 5MB
- Qualidade mínima de imagem recomendada: 320x240px

## Notas de Segurança

Para uso em produção:

1. Implemente autenticação e autorização
2. Valide e sanitize todas as entradas
3. Use HTTPS para todas as comunicações
4. Implemente rate limiting
5. Configure CORS adequadamente
6. Use variáveis de ambiente para configurações sensíveis
