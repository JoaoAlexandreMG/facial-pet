import io
import json
import os
from base64 import b64decode

import face_recognition
import numpy as np
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from PIL import Image
from werkzeug.utils import secure_filename

from db import close_connection, get_db, init_db

app = Flask(__name__)
app.secret_key = "facialpet2025"

# Configurações globais
ROSTOS_FILE = "rostos.npy"
FOTOS_FOLDER = "fotos"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

os.makedirs(FOTOS_FOLDER, exist_ok=True)

# ========== FUNÇÕES UTILITÁRIAS SIMPLIFICADAS ==========


def setup_db():
    """Inicializa o banco de dados"""
    init_db()


@app.teardown_appcontext
def teardown_db(exception):
    close_connection(exception)


def allowed_file(filename):
    """Verifica se o arquivo tem extensão permitida"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def carregar_rostos():
    """Carrega os rostos treinados"""
    if not os.path.exists(ROSTOS_FILE):
        return [], []

    try:
        data = np.load(ROSTOS_FILE, allow_pickle=True).item()
        return data.get("encodings", []), data.get("nomes", [])
    except Exception as e:
        flash(f"Erro ao carregar rostos: {e}", "danger")
        return [], []


def salvar_rostos(encodings, nomes):
    """Salva os rostos no arquivo"""
    try:
        np.save(ROSTOS_FILE, {"encodings": encodings, "nomes": nomes})
    except Exception as e:
        flash(f"Erro ao salvar rostos: {e}", "danger")


def salvar_imagem(img_data_url=None, file=None, nome=""):
    """Salva imagem da webcam ou arquivo"""
    if img_data_url:
        # Processa imagem da webcam
        header, encoded = img_data_url.split(",", 1)
        img_bytes = b64decode(encoded)
        filename = secure_filename(f"{nome}.jpg")
        path = os.path.join(FOTOS_FOLDER, filename)
        with open(path, "wb") as f:
            f.write(img_bytes)
        return True
    elif file and allowed_file(file.filename):
        # Processa arquivo enviado
        filename = secure_filename(f"{nome}.jpg")
        path = os.path.join(FOTOS_FOLDER, filename)
        file.save(path)
        return True
    return False


def treinar_rostos():
    """Treina o modelo com todas as fotos"""
    rostos_conhecidos = []
    nomes_conhecidos = []
    erros = []

    for arquivo in os.listdir(FOTOS_FOLDER):
        if arquivo.endswith(tuple(ALLOWED_EXTENSIONS)):
            nome = os.path.splitext(arquivo)[0]
            caminho = os.path.join(FOTOS_FOLDER, arquivo)

            try:
                imagem = face_recognition.load_image_file(caminho)
                encodings = face_recognition.face_encodings(imagem)
                if encodings:
                    rostos_conhecidos.append(encodings[0].tolist())
                    nomes_conhecidos.append(nome)
                else:
                    erros.append(arquivo)
            except Exception:
                erros.append(arquivo)

    salvar_rostos(rostos_conhecidos, nomes_conhecidos)
    return erros


def reconhecer_pessoa(img_data_url):
    """Reconhece uma pessoa na imagem"""
    if not img_data_url:
        return {"success": False, "msg": "Nenhuma imagem fornecida"}

    try:
        # Converte base64 para imagem
        header, encoded = img_data_url.split(",", 1)
        img_bytes = b64decode(encoded)
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        np_img = np.array(img)

        # Carrega rostos conhecidos
        encodings, nomes = carregar_rostos()
        if not encodings:
            return {"success": False, "msg": "Nenhum rosto cadastrado"}

        # Detecta rostos na imagem
        faces = face_recognition.face_encodings(np_img)
        if not faces:
            return {"success": True, "nome": "Nenhum rosto detectado"}

        # Compara com rostos conhecidos
        face_encoding = faces[0]
        distancias = face_recognition.face_distance(np.array(encodings), face_encoding)

        if len(distancias) == 0:
            return {"success": True, "nome": "Desconhecido"}

        melhor_match = np.argmin(distancias)
        if distancias[melhor_match] < 0.5:  # Limiar de confiança
            return {"success": True, "nome": nomes[melhor_match]}
        else:
            return {"success": True, "nome": "Desconhecido"}

    except Exception as e:
        return {"success": False, "msg": f"Erro no reconhecimento: {str(e)}"}


# ========== ROTAS PRINCIPAIS ==========


@app.route("/")
def index():
    """Página inicial - redireciona para eventos"""
    return redirect(url_for("eventos"))


@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    """Cadastra novo rosto"""
    if request.method == "POST":
        nome = request.form.get("nome")
        file = request.files.get("imagem")
        img_data_url = request.form.get("img_data_url")

        # Validação básica
        if not nome or (not file and not img_data_url):
            flash("Informe o nome e tire ou selecione uma imagem.", "warning")
            return redirect(request.url)

        # Salva a imagem
        if salvar_imagem(img_data_url, file, nome):
            # Treina os rostos
            erros = treinar_rostos()
            if erros:
                flash(
                    f"Imagem salva para {nome}, mas houve problemas com: {', '.join(erros)}",
                    "warning",
                )
            else:
                flash(f"Rosto de {nome} cadastrado com sucesso!", "success")
        else:
            flash("Formato de arquivo não suportado.", "danger")

        return redirect(request.url)

    return render_template("cadastrar.html")


@app.route("/gerenciar", methods=["GET", "POST"])
def gerenciar():
    """Gerencia participantes cadastrados"""
    db = get_db()
    participantes = db.execute("SELECT * FROM participante ORDER BY nome").fetchall()

    if request.method == "POST":
        excluir = request.form.getlist("excluir")
        if excluir:
            for participante_id in excluir:
                participante = db.execute(
                    "SELECT * FROM participante WHERE id = ?", (participante_id,)
                ).fetchone()

                if participante:
                    nome = participante["nome"]
                    # Remove foto
                    for ext in ALLOWED_EXTENSIONS:
                        foto_path = os.path.join(FOTOS_FOLDER, f"{nome}.{ext}")
                        if os.path.exists(foto_path):
                            try:
                                os.remove(foto_path)
                            except Exception as e:
                                flash(f"Erro ao remover foto: {e}", "warning")

                    # Remove do banco
                    db.execute(
                        "DELETE FROM participante WHERE id = ?", (participante_id,)
                    )
                    db.execute(
                        "DELETE FROM evento_participante WHERE participante_id = ?",
                        (participante_id,),
                    )
                    db.execute(
                        "DELETE FROM presenca WHERE participante_id = ?",
                        (participante_id,),
                    )

            db.commit()
            treinar_rostos()  # Atualiza modelo
            flash("Participante(s) excluído(s) com sucesso.", "success")

        return redirect(url_for("gerenciar"))

    return render_template("gerenciar.html", participantes=participantes)


@app.route("/foto/<nome>")
def foto(nome):
    """Serve foto de um participante"""
    for ext in ALLOWED_EXTENSIONS:
        path = os.path.join(FOTOS_FOLDER, f"{nome}.{ext}")
        if os.path.exists(path):
            return send_from_directory(FOTOS_FOLDER, f"{nome}.{ext}")
    return "", 404


@app.route("/reconhecer", methods=["GET", "POST"])
def reconhecer():
    """Reconhece pessoa em uma foto"""
    if request.method == "POST":
        img_data_url = request.form.get("img_data_url")
        resultado = reconhecer_pessoa(img_data_url)
        return resultado

    return render_template("reconhecer.html")


# ========== ROTAS DE EVENTOS ==========


@app.route("/eventos")
def eventos():
    """Lista todos os eventos"""
    db = get_db()
    eventos = db.execute("SELECT * FROM evento ORDER BY data_inicio DESC").fetchall()
    return render_template("eventos.html", eventos=eventos)


@app.route("/evento/novo", methods=["GET", "POST"])
def novo_evento():
    """Cria novo evento"""
    if request.method == "POST":
        nome = request.form["nome"]
        descricao = request.form.get("descricao")
        data_inicio = request.form.get("data_inicio")
        data_fim = request.form.get("data_fim")

        db = get_db()
        db.execute(
            "INSERT INTO evento (nome, descricao, data_inicio, data_fim) VALUES (?, ?, ?, ?)",
            (nome, descricao, data_inicio, data_fim),
        )
        db.commit()
        flash("Evento cadastrado com sucesso!", "success")
        return redirect(url_for("eventos"))

    return render_template("evento_form.html")


@app.route("/evento/<int:evento_id>")
def ver_evento(evento_id):
    """Mostra detalhes de um evento"""
    db = get_db()

    # Busca dados do evento
    evento = db.execute("SELECT * FROM evento WHERE id = ?", (evento_id,)).fetchone()
    momentos = db.execute(
        "SELECT * FROM momento WHERE evento_id = ? ORDER BY data, periodo", (evento_id,)
    ).fetchall()

    # Busca participantes
    todos_participantes = db.execute(
        "SELECT * FROM participante ORDER BY nome"
    ).fetchall()
    participantes = db.execute(
        """SELECT p.* FROM participante p
        JOIN evento_participante ep ON ep.participante_id = p.id WHERE ep.evento_id = ?""",
        (evento_id,),
    ).fetchall()

    # Prepara dados para o frontend
    todos_participantes = [dict(p) for p in todos_participantes]
    participantes_ids = [int(p["id"]) for p in participantes]
    participantes_disponiveis = [
        {"id": p["id"], "nome": p["nome"]}
        for p in todos_participantes
        if p["id"] not in participantes_ids
    ]

    # Calcula percentual de presença
    total_momentos = len(momentos)
    presencas = db.execute(
        "SELECT participante_id, COUNT(*) as total FROM presenca WHERE momento_id IN (SELECT id FROM momento WHERE evento_id = ?) GROUP BY participante_id",
        (evento_id,),
    ).fetchall()

    presenca_dict = {p["participante_id"]: p["total"] for p in presencas}
    percentuais = []
    for p in participantes:
        total_presencas = presenca_dict.get(p["id"], 0)
        percentual = (
            (total_presencas / total_momentos * 100) if total_momentos > 0 else 0
        )
        percentuais.append(
            {
                "nome": p["nome"],
                "percentual": percentual,
                "presencas": total_presencas,
                "total": total_momentos,
            }
        )

    return render_template(
        "evento_detalhe.html",
        evento=evento,
        momentos=momentos,
        participantes=participantes,
        todos_participantes=todos_participantes,
        participantes_ids=participantes_ids,
        percentuais=percentuais,
        participantes_disponiveis=json.dumps(
            participantes_disponiveis, ensure_ascii=False
        ),
    )


@app.route("/evento/<int:evento_id>/momento/novo", methods=["GET", "POST"])
def novo_momento(evento_id):
    """Cria novo momento em um evento"""
    if request.method == "POST":
        nome = request.form["nome"]
        data = request.form.get("data")
        periodo = request.form.get("periodo")

        db = get_db()
        db.execute(
            "INSERT INTO momento (evento_id, nome, data, periodo) VALUES (?, ?, ?, ?)",
            (evento_id, nome, data, periodo),
        )
        db.commit()
        flash("Momento cadastrado!", "success")
        return redirect(url_for("ver_evento", evento_id=evento_id))

    return render_template("momento_form.html", evento_id=evento_id)


@app.route("/evento/<int:evento_id>/excluir", methods=["POST"])
def excluir_evento(evento_id):
    """Exclui um evento e todos os seus dados"""
    db = get_db()

    # Remove dados relacionados
    momentos = db.execute(
        "SELECT id FROM momento WHERE evento_id = ?", (evento_id,)
    ).fetchall()
    for m in momentos:
        db.execute("DELETE FROM presenca WHERE momento_id = ?", (m["id"],))

    db.execute("DELETE FROM momento WHERE evento_id = ?", (evento_id,))
    db.execute("DELETE FROM evento_participante WHERE evento_id = ?", (evento_id,))
    db.execute("DELETE FROM evento WHERE id = ?", (evento_id,))
    db.commit()

    flash("Evento excluído com sucesso!", "success")
    return redirect(url_for("eventos"))


@app.route("/momento/<int:moment_id>/excluir", methods=["POST"])
def excluir_momento(moment_id):
    """Exclui um momento"""
    db = get_db()
    momento = db.execute("SELECT * FROM momento WHERE id = ?", (moment_id,)).fetchone()

    if not momento:
        flash("Momento não encontrado.", "warning")
        return redirect(url_for("eventos"))

    evento_id = momento["evento_id"]

    # Remove dados relacionados
    db.execute("DELETE FROM presenca WHERE momento_id = ?", (moment_id,))
    db.execute("DELETE FROM momento WHERE id = ?", (moment_id,))
    db.commit()

    flash("Momento excluído com sucesso!", "success")
    return redirect(url_for("ver_evento", evento_id=evento_id))


# ========== ROTAS DE PARTICIPANTES ==========


@app.route("/participantes")
def participantes():
    """Lista todos os participantes"""
    db = get_db()
    participantes = db.execute("SELECT * FROM participante ORDER BY nome").fetchall()
    return render_template("participantes.html", participantes=participantes)


@app.route("/participante/novo", methods=["GET", "POST"])
def novo_participante():
    """Cadastra novo participante"""
    evento_id = request.args.get("evento_id")

    if request.method == "POST":
        nome = request.form["nome"]
        file = request.files.get("imagem")
        img_data_url = request.form.get("img_data_url")

        # Validação
        if not nome or (not file and not img_data_url):
            flash("Informe o nome e tire ou selecione uma imagem.", "warning")
            return redirect(request.url)

        # Cadastra no banco
        db = get_db()
        cur = db.execute("INSERT INTO participante (nome) VALUES (?)", (nome,))
        participante_id = cur.lastrowid

        # Salva a foto
        if salvar_imagem(img_data_url, file, nome):
            # Vincula ao evento se necessário
            if evento_id:
                db.execute(
                    "INSERT INTO evento_participante (evento_id, participante_id) VALUES (?, ?)",
                    (evento_id, participante_id),
                )

            db.commit()

            # Treina os rostos
            erros = treinar_rostos()
            if erros:
                flash(
                    f"Participante cadastrado, mas houve problemas com: {', '.join(erros)}",
                    "warning",
                )
            else:
                flash("Participante cadastrado e treinado com sucesso!", "success")
        else:
            flash("Formato de arquivo não suportado.", "danger")
            return redirect(request.url)

        # Redireciona
        if evento_id:
            return redirect(url_for("ver_evento", evento_id=evento_id))
        return redirect(url_for("participantes"))

    return render_template("participante_form.html", evento_id=evento_id)


@app.route("/evento/<int:evento_id>/participante/adicionar", methods=["POST"])
def adicionar_participante_evento(evento_id):
    """Adiciona participante existente ao evento"""
    participante_id = request.form.get("participante_id")

    if not participante_id:
        flash("Selecione um participante para adicionar.", "warning")
        return redirect(url_for("ver_evento", evento_id=evento_id))

    db = get_db()
    db.execute(
        "INSERT INTO evento_participante (evento_id, participante_id) VALUES (?, ?)",
        (evento_id, participante_id),
    )
    db.commit()

    flash("Participante adicionado ao evento!", "success")
    return redirect(url_for("ver_evento", evento_id=evento_id))


# ========== ROTAS DE PRESENÇA ==========


@app.route("/presenca/<int:momento_id>", methods=["GET", "POST"])
def presenca(momento_id):
    """Controla presença em um momento"""
    db = get_db()

    # Busca dados
    momento = db.execute("SELECT * FROM momento WHERE id = ?", (momento_id,)).fetchone()
    evento = db.execute(
        "SELECT * FROM evento WHERE id = ?", (momento["evento_id"],)
    ).fetchone()
    participantes = db.execute(
        """SELECT p.* FROM participante p
        JOIN evento_participante ep ON ep.participante_id = p.id WHERE ep.evento_id = ?""",
        (evento["id"],),
    ).fetchall()
    presencas = db.execute(
        "SELECT participante_id FROM presenca WHERE momento_id = ?", (momento_id,)
    ).fetchall()
    presentes = set([p["participante_id"] for p in presencas])

    if request.method == "POST":
        participante_id = request.form["participante_id"]

        # Verifica se já está presente
        if int(participante_id) not in presentes:
            db.execute(
                "INSERT INTO presenca (momento_id, participante_id) VALUES (?, ?)",
                (momento_id, participante_id),
            )
            db.commit()
            flash("Presença registrada!", "success")
        else:
            flash("Participante já está presente!", "warning")

        return redirect(url_for("presenca", momento_id=momento_id))

    return render_template(
        "presenca.html",
        momento=momento,
        evento=evento,
        participantes=participantes,
        presentes=presentes,
    )


@app.route("/presenca/<int:momento_id>/reconhecer", methods=["POST"])
def reconhecer_presenca(momento_id):
    """Marca presença por reconhecimento facial"""
    db = get_db()

    # Busca dados do momento e evento
    momento = db.execute("SELECT * FROM momento WHERE id = ?", (momento_id,)).fetchone()
    evento = db.execute(
        "SELECT * FROM evento WHERE id = ?", (momento["evento_id"],)
    ).fetchone()
    participantes = db.execute(
        """SELECT p.* FROM participante p 
        JOIN evento_participante ep ON ep.participante_id = p.id 
        WHERE ep.evento_id = ?""",
        (evento["id"],),
    ).fetchall()

    # Cria dicionário de participantes
    participantes_dict = {p["nome"]: p for p in participantes}

    # Reconhece a pessoa
    img_data_url = request.form.get("img_data_url")
    resultado = reconhecer_pessoa(img_data_url)

    if not resultado["success"]:
        return resultado

    nome_reconhecido = resultado.get("nome")

    if nome_reconhecido in ["Nenhum rosto detectado", "Desconhecido"]:
        return {"success": True, "msg": nome_reconhecido}

    # Verifica se a pessoa está no evento
    participante = participantes_dict.get(nome_reconhecido)
    if not participante:
        return {
            "success": True,
            "msg": f"{nome_reconhecido} não está vinculado a este evento.",
        }

    # Verifica se já está presente
    presenca_existente = db.execute(
        "SELECT 1 FROM presenca WHERE momento_id = ? AND participante_id = ?",
        (momento_id, participante["id"]),
    ).fetchone()

    if presenca_existente:
        return {
            "success": True,
            "msg": f"{nome_reconhecido} já está marcado como presente.",
        }

    # Registra presença
    db.execute(
        "INSERT INTO presenca (momento_id, participante_id) VALUES (?, ?)",
        (momento_id, participante["id"]),
    )
    db.commit()

    return {"success": True, "msg": f"Presença de {nome_reconhecido} registrada!"}


# ========== INICIALIZAÇÃO ==========

if __name__ == "__main__":
    setup_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
