# ManuReport - Gerador de Relatórios de Manutenção

[![Deploy](https://img.shields.io/badge/Render-Deployed-brightgreen?style=for-the-badge&logo=render)](https://manureport.onrender.com)

**ManuReport** é uma aplicação web simples e eficiente para geração de relatórios técnicos de manutenção industrial. Ideal para empresas responsáveis por serviços ou equipes internas que precisam documentar ações corretivas, preventivas, preditivas e melhorias.

---

## 🚀 Funcionalidades

- Cadastro e autenticação de usuários
- Painel com dados da **empresa responsável** (ex-prestadora)
- Preenchimento dinâmico de formulário de manutenção com:
  - Dados do **cliente** (ex-tomadora)
  - Equipamento e criticidade
  - Descrição, causas, observações
  - Ações e pendências múltiplas
  - Logotipos com pré-visualização
- Geração de **relatório em HTML** e conversão automática para **PDF**
- Download do PDF gerado
- Início com duplo clique via `.bat` ou silencioso via `.vbs`

---

## 🌐 Demonstração Online

Acesse a aplicação online:  
➡️ **[manureport.onrender.com](https://manureport.onrender.com)**

## 🧩 Tecnologias Utilizadas

- Python 3.11+
- Flask 2.3
- Bootstrap 5.3
- Jinja2 (templates)
- WeasyPrint (PDF)
- Gunicorn (servidor WSGI)
- Render.com (deploy gratuito)

---

## 📂 Estrutura do Projeto

```bash
📁 manureport_web
├── app.py                       # Código principal do app
├── usuarios.json                # Dados de login (local)
├── empresa_responsavel.json    # Dados da empresa (local)
├── /relatorios                  # Relatórios gerados (local)
├── /static/logos                # Logotipos enviados
├── /templates                   # HTMLs renderizados
│   ├── login.html
│   ├── painel.html
│   ├── configurar_empresa.html
│   ├── editar_perfil.html
│   ├── alterar_senha.html
│   ├── formulario.html
│   └── relatorio.html
├── iniciar.bat                 # Inicia com terminal + navegador
├── manureport.vbs              # Inicia silenciosamente
├── requirements.txt            # Dependências
├── Procfile                    # Deploy na Render
└── .gitignore
```

---

## 🛠️ Como Executar Localmente

### Opção 1: Manualmente

```bash
# 1.Clone o repositório
git clone https://github.com/RBlaquez/manureport.git
cd manureport

# 2. Crie o ambiente virtual (opcional mas recomendado)
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute a aplicação
python app.py

# 5. Acesse em: http://127.0.0.1:5000
```

### Opção 2: Duplo Clique
- `iniciar.bat` → abre terminal + navegador

### Opção 3: Duplo Clique
- `manureport.vbs` → inicia silenciosamente

---

## 📄 Licença

Este projeto está sob a licença **MIT**.

---

Desenvolvido por **Rogério Blaquez**.
