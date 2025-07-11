from flask import Flask, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
print("📍 Base de datos creada en:", os.path.abspath("usuarios.db"))
app = Flask(__name__)
DB = 'usuarios.db'
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios (usuario TEXT, clave TEXT)''')
    conn.commit()
    conn.close()
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        clave = request.form['clave']
        hashed = generate_password_hash(clave)
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("INSERT INTO usuarios VALUES (?, ?)", (usuario, hashed))
        conn.commit()
        conn.close()
        return "Usuario guardado"
    return '''
        <form method="post">
            Usuario: <input type="text" name="usuario"><br>
            Clave: <input type="password" name="clave"><br>
            <input type="submit">
        </form>
    '''
if __name__ == '__main__':
    init_db()
    app.run(port=5800)
