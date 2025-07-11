# Facial PET 🎯

<div align="center">
  
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Sistema Web de Reconhecimento Facial para Controle de Presença**

Um sistema moderno e intuitivo para gerenciamento de eventos e controle de presença usando reconhecimento facial.

[Funcionalidades](#funcionalidades) • [Instalação](#instalação) • [Uso](#uso) • [API](#api) • [Contribuição](#contribuição)

</div>

## 📋 Sobre o Projeto

O **Facial PET** é um sistema web desenvolvido em Flask que permite o gerenciamento de eventos e controle de presença através de reconhecimento facial. O sistema oferece uma interface moderna e responsiva, facilitando o cadastro de participantes e o registro de presença de forma automatizada.

### 🎯 Objetivo

Facilitar o controle de presença em eventos, aulas ou reuniões, eliminando a necessidade de chamadas manuais e proporcionando uma experiência mais eficiente e moderna.

## ✨ Funcionalidades

### 🎪 Gerenciamento de Eventos
- ✅ Criação e edição de eventos
- ✅ Definição de período (data início/fim)
- ✅ Organização por momentos específicos
- ✅ Interface intuitiva para visualização

### 👥 Gestão de Participantes
- ✅ Cadastro de participantes com foto
- ✅ Captura via webcam ou upload de imagem
- ✅ Reconhecimento facial automático
- ✅ Gerenciamento de banco de rostos

### ⏰ Controle de Presença
- ✅ Registro manual via interface
- ✅ Reconhecimento facial automático
- ✅ Controle por momentos específicos
- ✅ Relatórios de presença em tempo real

### 🎨 Interface Moderna
- ✅ Design responsivo e minimalista
- ✅ Paleta de cores harmônica
- ✅ Experiência de usuário otimizada
- ✅ Compatibilidade com dispositivos móveis

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Descrição |
|------------|--------|-----------|
| **Python** | 3.8+ | Linguagem principal |
| **Flask** | 2.0+ | Framework web |
| **OpenCV** | 4.0+ | Processamento de imagem |
| **face_recognition** | Latest | Reconhecimento facial |
| **SQLite** | 3.0+ | Banco de dados |
| **Bootstrap** | 5.3 | Framework CSS |
| **jQuery** | 3.7+ | JavaScript |

## 📦 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Webcam (opcional, para captura de fotos)

### 1. Clone o Repositório

```bash
git clone https://github.com/JoaoAlexandreMG/facial-pet.git
cd facial-pet
```

### 2. Crie um Ambiente Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o Banco de Dados

```bash
python -c "from app import setup_db; setup_db()"
```

### 5. Execute a Aplicação

```bash
python app.py
```

A aplicação estará disponível em `http://localhost:5000`

## 🚀 Uso

### 1. Acesso ao Sistema

Abra seu navegador e acesse `http://localhost:5000`

### 2. Criando um Evento

1. Na página inicial, clique em "Novo Evento"
2. Preencha os dados do evento
3. Defina as datas de início e fim (opcional)
4. Salve o evento

### 3. Cadastrando Participantes

1. Acesse um evento específico
2. Clique em "Novo Participante"
3. Digite o nome do participante
4. Capture uma foto via webcam ou faça upload
5. Confirme o cadastro

### 4. Criando Momentos

1. No evento, clique em "Novo Momento"
2. Defina nome, data e período
3. Salve o momento

### 5. Registrando Presença

#### Manual:
1. Acesse o momento específico
2. Selecione o participante na lista
3. Clique em "Marcar Presença"

#### Por Reconhecimento:
1. Acesse o momento específico
2. Clique em "Reconhecer e Marcar Presença"
3. Posicione-se em frente à webcam
4. O sistema identificará automaticamente

## 🌐 Acesso Remoto

### Ngrok (Recomendado)

Para acessar o sistema remotamente:

```bash
# Instale o ngrok
# Execute a aplicação localmente
python app.py

# Em outro terminal
ngrok http 5000
```

### Rede Local

Para acesso na rede local, o sistema já está configurado para `0.0.0.0:5000`

## 📁 Estrutura do Projeto

```
facial-pet/
├── app.py                 # Aplicação principal Flask
├── db.py                  # Configuração do banco de dados
├── requirements.txt       # Dependências Python
├── facialpet.db          # Banco de dados SQLite
├── rostos.npy            # Dados de reconhecimento facial
├── fotos/                # Imagens dos participantes
├── static/
│   └── img/
│       └── logo.ico      # Ícone da aplicação
└── templates/            # Templates HTML
    ├── base.html         # Template base
    ├── eventos.html      # Lista de eventos
    ├── evento_detalhe.html # Detalhes do evento
    ├── evento_form.html  # Formulário de evento
    ├── participante_form.html # Cadastro de participante
    ├── momento_form.html # Formulário de momento
    ├── presenca.html     # Controle de presença
    ├── gerenciar.html    # Gerenciar participantes
    └── reconhecer.html   # Reconhecimento facial
```

## 🔧 API Endpoints

| Método | Endpoint | Descrição |
|---------|----------|-----------|
| `GET` | `/` | Página inicial (eventos) |
| `GET/POST` | `/evento/novo` | Criar novo evento |
| `GET` | `/evento/<id>` | Detalhes do evento |
| `POST` | `/evento/<id>/excluir` | Excluir evento |
| `GET/POST` | `/evento/<id>/momento/novo` | Criar momento |
| `GET/POST` | `/evento/<id>/participante/novo` | Novo participante |
| `GET/POST` | `/momento/<id>/presenca` | Controle de presença |
| `POST` | `/momento/<id>/presenca/reconhecer` | Reconhecimento facial |
| `GET/POST` | `/gerenciar` | Gerenciar participantes |

## 🔒 Configurações de Segurança

- **SECRET_KEY**: Altere a chave secreta em produção
- **Debug Mode**: Desative em ambiente de produção
- **CORS**: Configure adequadamente para acesso externo

## 🐛 Solução de Problemas

### Erro de Webcam
```bash
# Verifique as permissões do navegador
# Teste com: navigator.mediaDevices.getUserMedia()
```

### Erro de Reconhecimento
```bash
# Verifique a qualidade da imagem
# Certifique-se de que o rosto está bem iluminado
```

### Erro de Banco de Dados
```bash
# Recrie o banco de dados
python -c "from app import setup_db; setup_db()"
```

## 🤝 Contribuição

Contribuições são bem-vindas! Veja o arquivo [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes.

### Como Contribuir

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👥 Autores

- **João Alexandre** - *Desenvolvimento inicial* - [JoaoAlexandreMG](https://github.com/JoaoAlexandreMG)

## 🙏 Agradecimentos

- Biblioteca face_recognition por Adam Geitgey
- Comunidade Flask
- Bootstrap Team
- OpenCV Community

## 📞 Suporte

- 📧 Email: joao.alexandre@exemplo.com
- 💬 Issues: [GitHub Issues](https://github.com/JoaoAlexandreMG/facial-pet/issues)
- 📖 Documentação: [Wiki](https://github.com/JoaoAlexandreMG/facial-pet/wiki)

---

<div align="center">

**⭐ Se este projeto te ajudou, não esqueça de dar uma estrela! ⭐**

</div>
