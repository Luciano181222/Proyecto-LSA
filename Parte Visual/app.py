from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
import os
import re
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "usuarios.db")
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "cambia-esta-clave-en-produccion")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if "usuario_id" not in session:
            flash("Iniciá sesión para acceder al traductor.", "info")
            return redirect(url_for("login", next=request.path))
        return fn(*args, **kwargs)
    return wrapper

@app.route("/")
def index():
    return render_template("index.html", usuario=session.get("usuario_nombre"))

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if len(nombre) < 2:
            flash("Ingresá tu nombre (al menos 2 caracteres).", "error")
        elif not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            flash("Ingresá un correo electrónico válido.", "error")
        elif len(password) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.", "error")
        else:
            try:
                with get_db() as db:
                    cur = db.execute(
                        "INSERT INTO usuarios (nombre, email, password_hash) VALUES (?, ?, ?)",
                        (nombre, email, generate_password_hash(password))
                    )
                    user_id = cur.lastrowid
                session["usuario_id"] = user_id
                session["usuario_nombre"] = nombre
                session["usuario_email"] = email
                flash("¡Tu cuenta fue creada! Ya podés comenzar.", "success")
                return redirect(url_for("index") + "#traducir")
            except sqlite3.IntegrityError:
                flash("Ya existe una cuenta con ese correo.", "error")
    return render_template("auth.html", modo="registro")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        with get_db() as db:
            user = db.execute("SELECT * FROM usuarios WHERE email = ?", (email,)).fetchone()
        if user and check_password_hash(user["password_hash"], password):
            session.clear()
            session["usuario_id"] = user["id"]
            session["usuario_nombre"] = user["nombre"]
            session["usuario_email"] = user["email"]
            flash(f"¡Hola, {user['nombre']}! Iniciaste sesión correctamente.", "success")
            target = request.args.get("next")
            return redirect(target if target and target.startswith("/") else url_for("index") + "#traducir")
        flash("Correo o contraseña incorrectos.", "error")
    return render_template("auth.html", modo="login")

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("Cerraste sesión.", "info")
    return redirect(url_for("index"))

@app.route("/traductor")
@login_required
def traductor():
    return render_template("translator.html", usuario=session.get("usuario_nombre"))

@app.route("/api/estado")
def estado():
    return jsonify({"autenticado": "usuario_id" in session,
                    "usuario": session.get("usuario_nombre")})

@app.after_request
def security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
