from flask import Flask, render_template, request, send_from_directory, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import base64
import json
from weasyprint import HTML
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "chave_super_segura_123"

PASTA_RELATORIOS = "relatorios"
ARQUIVO_USUARIOS = "usuarios.json"

if not os.path.exists(PASTA_RELATORIOS):
    os.makedirs(PASTA_RELATORIOS)

# ========================
# Funções auxiliares
# ========================
def carregar_usuarios():
    if os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_usuario(username, senha_hash):
    usuarios = carregar_usuarios()
    usuarios[username] = senha_hash
    with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as f:
        json.dump(usuarios, f)

# Função para carregar os dados da empresa responsavel
def carregar_dados_empresa_responsavel():
    if os.path.exists("empresa_responsavel.json"):
        with open("empresa_responsavel.json", "r", encoding="utf-8") as f:
            empresa_responsavel = json.load(f)
            # Carregar o logo em base64 se houver
            if os.path.exists("logo_empresa_responsavel.bmp"):
                with open("logo_empresa_responsavel.bmp", "rb") as logo_file:
                    empresa_responsavel['empresa_logotipo'] = "data:image/bmp;base64," + base64.b64encode(logo_file.read()).decode('utf-8')
            return empresa_responsavel
    return {}
    
# Função para garantir que o diretório de logos exista
def criar_diretorio_logos():
    pasta_logos = os.path.join("static", "logos")
    if not os.path.exists(pasta_logos):
        os.makedirs(pasta_logos)
    return pasta_logos

# Função para salvar o logo da empresa
def salvar_logo_empresa(arquivo):
    # Certifique-se de que o diretório de logos exista
    pasta_logos = criar_diretorio_logos()

    # Salvar o logo da empresa
    caminho_logo = os.path.join(pasta_logos, secure_filename(arquivo.filename))
    arquivo.save(caminho_logo)
    return caminho_logo

# Função para salvar os dados da empresa responsavel
def salvar_dados_empresa_responsavel(dados):
    with open("empresa_responsavel.json", "w", encoding="utf-8") as f:
        json.dump(dados, f)
        
# ========================
# Rotas principais
# ========================
@app.route("/", methods=["GET"])
def index():
    if "usuario" in session:
        return redirect(url_for("painel"))
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    senha = request.form["password"]
    usuarios = carregar_usuarios()
    if username in usuarios and check_password_hash(usuarios[username], senha):
        session["usuario"] = username
        flash("Login realizado com sucesso!", "success")
        return redirect(url_for("painel"))
    flash("Usuário ou senha inválidos.", "danger")
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    flash("Você saiu com sucesso.", "info")
    return redirect(url_for("index"))

@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        username = request.form["username"]
        senha = request.form["password"]
        confirmar = request.form["confirm"]

        if senha != confirmar:
            flash("As senhas não coincidem.", "danger")
            return redirect(url_for("registrar"))

        usuarios = carregar_usuarios()
        if username in usuarios:
            flash("Usuário já existe.", "warning")
            return redirect(url_for("registrar"))

        senha_hash = generate_password_hash(senha)
        salvar_usuario(username, senha_hash)
        flash("Usuário registrado com sucesso!", "success")
        return redirect(url_for("index"))

    return render_template("registrar.html")

@app.route("/painel")
def painel():
    if "usuario" not in session:
        flash("Faça login para acessar o painel.", "warning")
        return redirect(url_for("index"))

    # Carregar dados da empresa responsavel
    empresa_responsavel = carregar_dados_empresa_responsavel()

    # Passar os dados para o template
    dados = {
        "empresa_nome": empresa_responsavel.get("empresa_nome", ""),
        "empresa_cnpj": empresa_responsavel.get("empresa_cnpj", ""),
        "empresa_endereco": empresa_responsavel.get("empresa_endereco", ""),
        "empresa_telefone": empresa_responsavel.get("empresa_telefone", ""),
        "empresa_email": empresa_responsavel.get("empresa_email", ""),
        "empresa_logotipo": empresa_responsavel.get("empresa_logotipo", "")
    }

    return render_template("painel.html", dados=dados)
    
@app.route("/editar_perfil", methods=["GET", "POST"])
def editar_perfil():
    if "usuario" not in session:
        flash("Acesso não autorizado. Faça login.", "danger")
        return redirect(url_for("index"))
    
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        
        # Lógica para salvar as novas informações do perfil (pode ser em um arquivo ou banco de dados)
        
        flash("Perfil atualizado com sucesso!", "success")
        return redirect(url_for("painel"))

    return render_template("editar_perfil.html")
    
@app.route("/alterar_senha", methods=["GET", "POST"])
def alterar_senha():
    if "usuario" not in session:
        flash("Acesso não autorizado. Faça login.", "danger")
        return redirect(url_for("index"))
    
    if request.method == "POST":
        senha_atual = request.form["senha_atual"]
        nova_senha = request.form["nova_senha"]
        confirmar_senha = request.form["confirmar_senha"]

        usuarios = carregar_usuarios()
        usuario_atual = session["usuario"]

        if usuario_atual not in usuarios:
            flash("Usuário não encontrado.", "danger")
            return redirect(url_for("alterar_senha"))

        if not check_password_hash(usuarios[usuario_atual], senha_atual):
            flash("Senha atual incorreta.", "danger")
            return redirect(url_for("alterar_senha"))

        if nova_senha != confirmar_senha:
            flash("As novas senhas não coincidem.", "warning")
            return redirect(url_for("alterar_senha"))

        # Atualiza a senha no arquivo JSON
        usuarios[usuario_atual] = generate_password_hash(nova_senha)
        with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as f:
            json.dump(usuarios, f)

        flash("Senha alterada com sucesso!", "success")
        return redirect(url_for("painel"))
    
    return render_template("alterar_senha.html")

@app.route("/formulario", methods=["GET", "POST"])
def formulario():
    if "usuario" not in session:
        flash("Acesso não autorizado. Faça login.", "danger")
        return redirect(url_for("index"))

    empresa_responsavel = carregar_dados_empresa_responsavel()
    
    if request.method == "POST":
        dados = request.form.to_dict()
        dados["empresa_responsavel_nome"] = empresa_responsavel.get("empresa_nome", "")
        dados["empresa_responsavel_cnpj"] = empresa_responsavel.get("empresa_cnpj", "")
        dados["empresa_responsavel_endereco"] = empresa_responsavel.get("empresa_endereco", "")
        dados["empresa_responsavel_telefone"] = empresa_responsavel.get("empresa_telefone", "")
        dados["empresa_responsavel_email"] = empresa_responsavel.get("empresa_email", "")

        # Logo da empresa responsavel (de arquivo)
        if "empresa_logotipo" in empresa_responsavel:
            logo_responsavel = os.path.join("static", "logos", empresa_responsavel["empresa_logotipo"])
            if os.path.exists(logo_responsavel):
                with open(logo_responsavel, "rb") as img_file:
                    dados["logo_responsavel_base64"] = "data:image/png;base64," + base64.b64encode(img_file.read()).decode("utf-8")

        # Logo da empresa cliente (do formulário)
        if "logotipo" in request.files:
            logo_cliente = request.files["logotipo"]
            if logo_cliente and logo_cliente.filename != "":
                nome_logo_cliente = secure_filename(logo_cliente.filename)
                caminho_logo_cliente = os.path.join("static", "logos", nome_logo_cliente)
                logo_cliente.save(caminho_logo_cliente)

                with open(caminho_logo_cliente, "rb") as f:
                    dados["logo_cliente_base64"] = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

        # Ações e pendências
        dados["acoes"] = list(zip(
            request.form.getlist("acao_Descrição[]"),
            request.form.getlist("acao_Data Início[]"),request.files,
            request.form.getlist("acao_Hora Início[]"),
            request.form.getlist("acao_Data Fim[]"),
            request.form.getlist("acao_Hora Fim[]")
        ))
        dados["pendencias"] = request.form.getlist("pendencia_Descrição[]")

        # Gerar nome do arquivo
        nome_relatorio = f"relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        dados["nome_arquivo"] = nome_relatorio

        # Gera e salva o PDF
        html = render_template("relatorio.html", dados=dados, gerar_pdf=True)
        caminho_arquivo = os.path.join(PASTA_RELATORIOS, nome_relatorio)
        HTML(string=html).write_pdf(caminho_arquivo)

        return render_template("relatorio.html", dados=dados)

    return render_template("formulario.html", dados={}, gerar=False, idioma="pt-BR")

@app.route("/configurar_empresa", methods=["GET", "POST"])
def configurar_empresa():
    if "usuario" not in session:
        flash("Acesso não autorizado. Faça login.", "danger")
        return redirect(url_for("index"))
    
    # Carregar dados da empresa responsavel
    empresa_responsavel = carregar_dados_empresa_responsavel()

    if request.method == "POST":
        dados_empresa = {
            "empresa_nome": request.form["empresa_nome"],
            "empresa_cnpj": request.form["empresa_cnpj"],
            "empresa_endereco": request.form["empresa_endereco"],
            "empresa_telefone": request.form["empresa_telefone"],
            "empresa_email": request.form["empresa_email"]
        }

        # Verificar se foi enviado um logo
        if "logo_empresa" in request.files:
            logo_arquivo = request.files["logo_empresa"]
            if logo_arquivo.filename != "":
               nome_arquivo = secure_filename(logo_arquivo.filename)
               salvar_logo_empresa(logo_arquivo)  # já salva no lugar certo
               dados_empresa["empresa_logotipo"] = nome_arquivo

        # Salvar dados no arquivo JSON
        salvar_dados_empresa_responsavel(dados_empresa)
        
        flash("Dados da empresa responsavel atualizados com sucesso!", "success")
        return redirect(url_for("painel"))
    
    return render_template("configurar_empresa.html", dados_empresa=empresa_responsavel)

@app.route("/relatorios/<filename>")
def relatorio_gerado(filename):
    return send_from_directory(PASTA_RELATORIOS, filename)
    
@app.route("/baixar_pdf/<filename>")
def baixar_pdf(filename):
    return send_from_directory(PASTA_RELATORIOS, filename)

if __name__ == "__main__":
    app.run(debug=True)