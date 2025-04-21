# ManuReport - Gerador de Relatórios de Manutenção

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

## 🧩 Tecnologias Utilizadas

- **Python 3.11+**
- **Flask** (framework web)
- **Bootstrap 5** (design responsivo)
- **Jinja2** (templates)
- **WeasyPrint** (geração de PDF)

---

## 📂 Estrutura do Projeto

```bash
📁 manureport_web
├── app.py
├── usuarios.json
├── empresa_responsavel.json
├── /relatorios
├── /static
│   └── /logos
├── /templates
│   ├── login.html
│   ├── painel.html
│   ├── configurar_empresa.html
│   ├── editar_perfil.html
│   ├── alterar_senha.html
│   ├── formulario.html
│   └── relatorio.html
├── iniciar.bat
├── manureport.vbs
├── README.md
├── requirements.txt
└── .gitignore
```

---

## 🛠️ Como Executar

### Opção 1: Manualmente

```bash
# 1. Crie o ambiente virtual (opcional mas recomendado)
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute a aplicação
python app.py

# Acesse em: http://127.0.0.1:5000
```

### Opção 2: Duplo Clique
- `iniciar.bat` → abre terminal + navegador

### Opção 3: Duplo Clique
- `manureport.vbs` → inicia silenciosamente

---

Desenvolvido por **Rogério Blaquez**.
