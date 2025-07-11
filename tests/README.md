# Testes - Facial PET

Este diretório contém todos os testes automatizados do sistema Facial PET.

## Estrutura de Testes

```
tests/
├── __init__.py
├── conftest.py                 # Configurações do pytest
├── test_app.py                 # Testes da aplicação Flask
├── test_db.py                  # Testes do banco de dados
├── test_facial_recognition.py  # Testes de reconhecimento facial
├── test_models.py              # Testes dos modelos de dados
├── test_utils.py               # Testes de funções utilitárias
├── fixtures/                   # Dados de teste
│   ├── images/                 # Imagens para teste
│   └── test_data.json         # Dados de exemplo
└── integration/                # Testes de integração
    ├── test_workflows.py       # Fluxos completos
    └── test_api.py             # Testes da API
```

## Executando os Testes

### Instalação das Dependências de Teste

```bash
pip install pytest pytest-cov pytest-flask
```

### Executar Todos os Testes

```bash
pytest
```

### Executar com Cobertura

```bash
pytest --cov=app --cov-report=html
```

### Executar Testes Específicos

```bash
# Testar apenas reconhecimento facial
pytest tests/test_facial_recognition.py

# Testar com verbosidade
pytest -v

# Testar e parar no primeiro erro
pytest -x
```

## Tipos de Teste

### 1. Testes Unitários
- Testam funções individuais isoladamente
- Usam mocks para dependências externas
- Rápidos de executar

### 2. Testes de Integração
- Testam interação entre componentes
- Usam banco de dados de teste
- Verificam fluxos completos

### 3. Testes de Interface
- Testam rotas Flask
- Verificam renderização de templates
- Simulam requisições HTTP

## Configuração de Teste

### conftest.py
```python
import pytest
import tempfile
import os
from app import app, setup_db

@pytest.fixture
def client():
    # Criar banco temporário para testes
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        with app.app_context():
            setup_db()
        yield client
    
    os.close(db_fd)
    os.unlink(app.config['DATABASE'])

@pytest.fixture
def sample_image():
    # Retorna caminho para imagem de teste
    return 'tests/fixtures/images/sample_face.jpg'
```

## Dados de Teste

### Imagens de Teste
- Rostos conhecidos para reconhecimento
- Imagens sem rostos
- Formatos diferentes (JPG, PNG)
- Tamanhos variados

### Dados JSON
```json
{
  "eventos": [
    {
      "nome": "Evento Teste",
      "descricao": "Descrição do evento de teste",
      "data_inicio": "2025-01-01",
      "data_fim": "2025-01-02"
    }
  ],
  "participantes": [
    {
      "nome": "João Teste",
      "imagem": "tests/fixtures/images/joao.jpg"
    }
  ]
}
```

## Boas Práticas

### Nomenclatura
- Nomes descritivos: `test_should_create_event_when_valid_data()`
- Padrão AAA: Arrange, Act, Assert

### Isolamento
- Cada teste deve ser independente
- Use fixtures para setup/teardown
- Limpe dados após cada teste

### Cobertura
- Objetivo: > 80% de cobertura
- Foque em caminhos críticos
- Teste casos de erro

## Executar Testes em CI/CD

### GitHub Actions
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: pytest --cov=app --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v1
```

## Mocking

### Reconhecimento Facial
```python
@patch('face_recognition.face_encodings')
@patch('face_recognition.compare_faces')
def test_facial_recognition_mock(mock_compare, mock_encodings):
    mock_encodings.return_value = [np.array([1, 2, 3])]
    mock_compare.return_value = [True]
    
    # Seu teste aqui
```

### Banco de Dados
```python
@patch('app.get_db')
def test_with_mock_db(mock_get_db):
    mock_db = MagicMock()
    mock_get_db.return_value = mock_db
    
    # Seu teste aqui
```

## Performance Testing

### Teste de Carga
```python
import time

def test_facial_recognition_performance():
    start_time = time.time()
    
    # Executar reconhecimento facial
    result = recognize_face(test_image)
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    # Verificar se executou em menos de 1 segundo
    assert execution_time < 1.0
```

## Relatórios de Teste

### HTML Coverage Report
```bash
pytest --cov=app --cov-report=html
# Gera htmlcov/index.html
```

### XML Report (para CI)
```bash
pytest --cov=app --cov-report=xml --junitxml=test-results.xml
```

## Debugging de Testes

### Usar pdb
```python
def test_debug_example():
    import pdb; pdb.set_trace()
    # Seu código de teste
```

### Logs durante testes
```python
import logging
logging.basicConfig(level=logging.DEBUG)

def test_with_logs():
    logger = logging.getLogger(__name__)
    logger.debug("Debug info durante teste")
```

## Testes Específicos do Facial PET

### Reconhecimento Facial
- Teste com rostos conhecidos
- Teste com rostos desconhecidos
- Teste com múltiplos rostos
- Teste com imagens inválidas

### Controle de Presença
- Marcar presença manual
- Marcar presença por reconhecimento
- Evitar duplicatas
- Validar participantes do evento

### Gerenciamento de Eventos
- Criar, editar, excluir eventos
- Adicionar momentos
- Associar participantes
- Validar datas

Mantenha os testes atualizados conforme o código evolui!
