# Guia de Instalação - Facial PET

Este guia fornece instruções detalhadas para instalar e configurar o sistema Facial PET.

## Índice

- [Requisitos do Sistema](#requisitos-do-sistema)
- [Instalação Local](#instalação-local)
- [Configuração do Banco de Dados](#configuração-do-banco-de-dados)
- [Configuração do Ambiente](#configuração-do-ambiente)
- [Instalação em Produção](#instalação-em-produção)
- [Solução de Problemas](#solução-de-problemas)

## Requisitos do Sistema

### Requisitos Mínimos

- **Sistema Operacional**: Windows 10+, macOS 10.14+, ou Linux Ubuntu 18.04+
- **Python**: 3.8 ou superior
- **RAM**: 4GB mínimo, 8GB recomendado
- **Espaço em Disco**: 2GB livre
- **Webcam**: Opcional (para captura de fotos)

### Dependências do Sistema

#### Windows

```bash
# Instalar Microsoft Visual C++ Build Tools
# Download: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Instalar CMake (necessário para dlib)
# Download: https://cmake.org/download/
```

#### macOS

```bash
# Instalar Homebrew se não tiver
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar dependências
brew install cmake
brew install python@3.9
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
sudo apt install build-essential cmake
sudo apt install libopencv-dev python3-opencv
sudo apt install libboost-all-dev
```

## Instalação Local

### 1. Clone o Repositório

```bash
git clone https://github.com/seu-usuario/facial-pet.git
cd facial-pet
```

### 2. Criar Ambiente Virtual

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Atualizar pip

```bash
python -m pip install --upgrade pip
```

### 4. Instalar Dependências

```bash
pip install -r requirements.txt
```

**Nota**: Se encontrar erros com `dlib` ou `face_recognition`, consulte a [seção de solução de problemas](#solução-de-problemas).

### 5. Configurar Banco de Dados

```bash
python -c "from app import setup_db; setup_db()"
```

### 6. Executar a Aplicação

```bash
python app.py
```

A aplicação estará disponível em `http://localhost:5000`

## Configuração do Banco de Dados

### SQLite (Padrão)

O sistema usa SQLite por padrão, que não requer configuração adicional. O arquivo `facialpet.db` será criado automaticamente.

### PostgreSQL (Produção)

Para usar PostgreSQL em produção:

1. Instale o PostgreSQL
2. Crie um banco de dados:

```sql
CREATE DATABASE facialpet;
CREATE USER facialpet_user WITH PASSWORD 'sua_senha';
GRANT ALL PRIVILEGES ON DATABASE facialpet TO facialpet_user;
```

3. Configure a variável de ambiente:

```bash
export DATABASE_URL="postgresql://facialpet_user:sua_senha@localhost/facialpet"
```

4. Modifique `db.py` para usar PostgreSQL:

```python
import os
import psycopg2
from flask import g

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///facialpet.db')

def get_db():
    if 'postgresql://' in DATABASE_URL:
        # Configuração PostgreSQL
        db = psycopg2.connect(DATABASE_URL)
    else:
        # Configuração SQLite (padrão)
        db = sqlite3.connect(DATABASE_URL.replace('sqlite:///', ''))
    return db
```

## Configuração do Ambiente

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Configurações básicas
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=sua_chave_secreta_muito_forte

# Configurações do banco de dados
DATABASE_URL=sqlite:///facialpet.db

# Configurações de upload
MAX_CONTENT_LENGTH=16777216  # 16MB
UPLOAD_FOLDER=fotos

# Configurações de reconhecimento facial
FACE_RECOGNITION_TOLERANCE=0.6
MAX_FACES_PER_IMAGE=1

# Configurações de rede
HOST=0.0.0.0
PORT=5000
```

### Carregar Variáveis de Ambiente

Modifique `app.py` para carregar as variáveis:

```python
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'facialpet2025')
app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get('MAX_CONTENT_LENGTH', '16777216'))
```

### Instalar python-dotenv

```bash
pip install python-dotenv
```

## Instalação em Produção

### Usando Docker

1. Crie um `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopencv-dev \
    python3-opencv \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar diretórios necessários
RUN mkdir -p fotos

# Configurar banco de dados
RUN python -c "from app import setup_db; setup_db()"

EXPOSE 5000

CMD ["python", "app.py"]
```

2. Criar `docker-compose.yml`:

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./fotos:/app/fotos
      - ./facialpet.db:/app/facialpet.db
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=sua_chave_secreta_super_forte
```

3. Executar:

```bash
docker-compose up -d
```

### Usando Gunicorn

1. Instalar Gunicorn:

```bash
pip install gunicorn
```

2. Criar arquivo `wsgi.py`:

```python
from app import app

if __name__ == "__main__":
    app.run()
```

3. Executar com Gunicorn:

```bash
gunicorn --bind 0.0.0.0:5000 wsgi:app
```

### Configuração com Nginx

1. Configuração do Nginx (`/etc/nginx/sites-available/facialpet`):

```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Configuração para arquivos estáticos
    location /static {
        alias /caminho/para/facial-pet/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Configuração para fotos
    location /fotos {
        alias /caminho/para/facial-pet/fotos;
        expires 1d;
    }
}
```

2. Ativar site:

```bash
sudo ln -s /etc/nginx/sites-available/facialpet /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Solução de Problemas

### Erro na Instalação do dlib

#### Windows

```bash
# Opção 1: Usar wheel pré-compilado
pip install https://github.com/z-mahmud22/Dlib_Windows_Python3.x/raw/main/dlib-19.22.0-cp39-cp39-win_amd64.whl

# Opção 2: Usar conda
conda install -c conda-forge dlib
```

#### macOS

```bash
# Instalar dependências via Homebrew
brew install dlib
pip install dlib
```

#### Linux

```bash
# Instalar dependências
sudo apt-get install build-essential cmake
sudo apt-get install libopenblas-dev liblapack-dev 
sudo apt-get install libx11-dev libgtk-3-dev

pip install dlib
```

### Erro na Instalação do face_recognition

```bash
# Instalar dlib primeiro
pip install dlib

# Depois instalar face_recognition
pip install face_recognition
```

### Erro de Webcam

#### Linux

```bash
# Verificar dispositivos de vídeo
ls /dev/video*

# Adicionar usuário ao grupo de vídeo
sudo usermod -a -G video $USER
```

#### Permissões do Navegador

1. Acesse as configurações do navegador
2. Vá para Privacidade e Segurança
3. Permita acesso à câmera para o site

### Erro de Memória

Se o sistema apresentar erros de memória:

1. Aumente o tamanho do swap:

```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

2. Reduza a tolerância de reconhecimento facial no código:

```python
# Em app.py, reduza o valor para usar menos memória
known_face_encodings = face_recognition.face_encodings(image, model='small')
```

### Erro de Porta em Uso

```bash
# Encontrar processo usando a porta 5000
lsof -i :5000

# Matar processo
kill -9 PID_DO_PROCESSO

# Usar outra porta
python app.py --port 5001
```

### Problemas de Performance

1. **Otimizar reconhecimento facial**:

```python
# Reduzir qualidade da imagem para processamento mais rápido
image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
```

2. **Usar cache para encodings**:

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_face_encoding(image_path):
    # Cache encodings para evitar reprocessamento
    pass
```

### Logs para Debug

Adicione logging detalhado:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# No código
logger.debug(f"Processando imagem: {filename}")
logger.error(f"Erro no reconhecimento: {str(e)}")
```

## Suporte

Se ainda encontrar problemas:

1. Verifique os [issues existentes](https://github.com/seu-usuario/facial-pet/issues)
2. Crie um novo issue com detalhes do erro
3. Inclua informações do sistema e logs de erro
4. Entre em contato: seu-email@exemplo.com
