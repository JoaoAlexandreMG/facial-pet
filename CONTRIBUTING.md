# Contribuindo para o Facial PET

Primeiro de tudo, obrigado por considerar contribuir para o Facial PET! 🎉

Seguindo estas diretrizes, você nos ajuda a comunicar que você respeita o tempo dos desenvolvedores que gerenciam e desenvolvem este projeto de código aberto. Em troca, eles devem retribuir essa cortesia ao abordar seu problema, avaliar mudanças e ajudá-lo a finalizar seus pull requests.

## Como posso contribuir?

### Reportando Bugs

Esta seção te orienta através do envio de um relatório de bug para o Facial PET. Seguir essas diretrizes ajuda os mantenedores e a comunidade a entender seu relatório, reproduzir o comportamento e encontrar relatórios relacionados.

**Antes de criar relatórios de bug**, por favor verifique se o problema já não foi reportado.

#### Como enviar um (bom) relatório de bug?

Bugs são rastreados como [GitHub issues](https://github.com/seu-usuario/facial-pet/issues). Crie um issue e forneça as seguintes informações:

* **Use um título claro e descritivo** para o issue para identificar o problema.
* **Descreva os passos exatos que reproduzem o problema** com o máximo de detalhes possível.
* **Forneça exemplos específicos para demonstrar os passos**.
* **Descreva o comportamento que você observou após seguir os passos** e aponte qual é exatamente o problema com esse comportamento.
* **Explique qual comportamento você esperava ver e por quê.**
* **Inclua screenshots e GIFs animados** se possível.

### Sugerindo Melhorias

Esta seção te orienta através do envio de uma sugestão de melhoria para o Facial PET, incluindo funcionalidades completamente novas e pequenas melhorias à funcionalidade existente.

#### Como envio uma (boa) sugestão de melhoria?

Sugestões de melhoria são rastreadas como [GitHub issues](https://github.com/seu-usuario/facial-pet/issues). Crie um issue e forneça as seguintes informações:

* **Use um título claro e descritivo** para o issue para identificar a sugestão.
* **Forneça uma descrição passo-a-passo da melhoria sugerida** com o máximo de detalhes possível.
* **Forneça exemplos específicos para demonstrar os passos**.
* **Descreva o comportamento atual** e **explique qual comportamento você esperaria ver** e por quê.
* **Explique por que essa melhoria seria útil** para a maioria dos usuários do Facial PET.

### Seu Primeiro Código de Contribuição

Não tem certeza por onde começar a contribuir para o Facial PET? Você pode começar olhando para estes issues `beginner` e `help-wanted`:

* [Beginner issues](https://github.com/seu-usuario/facial-pet/labels/beginner) - issues que devem precisar de apenas algumas linhas de código, e um teste ou dois.
* [Help wanted issues](https://github.com/seu-usuario/facial-pet/labels/help%20wanted) - issues que devem ser um pouco mais envolvidos que issues `beginner`.

### Pull Requests

O processo descrito aqui tem vários objetivos:

- Manter a qualidade do Facial PET
- Corrigir problemas que são importantes para os usuários
- Engajar a comunidade trabalhando em direção ao melhor Facial PET possível
- Permitir um sistema sustentável para os mantenedores do Facial PET revisarem contribuições

Por favor siga estes passos para ter sua contribuição considerada pelos mantenedores:

1. Siga o [guia de estilo](#guia-de-estilo)
2. Após submeter seu pull request, verifique se todos os [status checks](https://help.github.com/articles/about-status-checks/) estão passando

Enquanto os pré-requisitos acima devem ser satisfeitos antes de ter seu pull request revisado, o(s) revisor(es) pode(m) pedir que você complete trabalho de design adicional, testes, ou outras mudanças antes que seu pull request possa ser finalmente aceito.

## Guia de Estilo

### Mensagens de Commit do Git

* Use o tempo presente ("Add feature" não "Added feature")
* Use o modo imperativo ("Move cursor to..." não "Moves cursor to...")
* Limite a primeira linha a 72 caracteres ou menos
* Referencie issues e pull requests liberalmente após a primeira linha
* Considere começar a mensagem de commit com um emoji aplicável:
    * 🎨 `:art:` quando melhorando o formato/estrutura do código
    * 🐎 `:racehorse:` quando melhorando performance
    * 📝 `:memo:` quando escrevendo docs
    * 🐛 `:bug:` quando corrigindo um bug
    * 🔥 `:fire:` quando removendo código ou arquivos
    * 💚 `:green_heart:` quando corrigindo o CI build
    * ✅ `:white_check_mark:` quando adicionando testes
    * 🔒 `:lock:` quando lidando com segurança
    * ⬆️ `:arrow_up:` quando atualizando dependências
    * ⬇️ `:arrow_down:` quando fazendo downgrade de dependências

### Guia de Estilo Python

* Siga a [PEP 8](https://www.python.org/dev/peps/pep-0008/)
* Use [Black](https://github.com/psf/black) para formatação de código
* Use [flake8](https://flake8.pycqa.org/) para linting
* Use type hints quando possível
* Docstrings devem seguir o [Google Style](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)

### Guia de Estilo JavaScript

* Use ponto e vírgula
* Use aspas simples para strings
* Use nomes descritivos para variáveis e funções
* Comente código complexo

### Guia de Estilo HTML/CSS

* Use indentação de 2 espaços
* Use classes CSS semânticas
* Prefira CSS flexbox e grid para layout
* Use Bootstrap classes quando possível

## Configuração do Ambiente de Desenvolvimento

1. Fork o repositório
2. Clone seu fork localmente
3. Configure o ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
4. Instale dependências de desenvolvimento:
   ```bash
   pip install -r requirements.txt
   pip install black flake8 pytest
   ```
5. Configure o banco de dados:
   ```bash
   python -c "from app import setup_db; setup_db()"
   ```
6. Execute os testes:
   ```bash
   pytest
   ```

## Estrutura de Branches

* `main` - Branch principal, sempre estável
* `develop` - Branch de desenvolvimento
* `feature/nome-da-feature` - Branches para novas funcionalidades
* `bugfix/nome-do-bug` - Branches para correção de bugs
* `hotfix/nome-do-hotfix` - Branches para correções urgentes

## Processo de Review

1. Todos os PRs devem ser revisados por pelo menos um mantenedor
2. PRs devem incluir testes para novas funcionalidades
3. PRs devem passar em todos os testes automatizados
4. PRs devem incluir documentação atualizada quando aplicável

## Questões?

Não hesite em abrir um issue se você tem questões sobre como contribuir!

## Reconhecimentos

Este guia de contribuição foi adaptado do [template open-source do Atom](https://github.com/atom/atom/blob/master/CONTRIBUTING.md).
