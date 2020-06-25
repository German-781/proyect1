import os

from models import *

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from flask import Flask, render_template, request

app = Flask(__name__)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hello", methods=["POST"])
def hello():
    nombre = request.form.get("nombre")
    passw = request.form.get("passw")

    user = db.execute("SELECT * FROM usuarios WHERE nombre = ('" + nombre + "') AND passw = ('" + passw + "')").first()
    if user is None:
       return render_template("error.html", mensaje= "password no corresponde")
    return render_template("error.html", mensaje= "conexion  O.K")
   
    #if db.execute("SELECT * FROM usuarios WHERE nombre = :nombre",{"nombre": nombre}).rowcount == 0:
    
    #   db.execute("INSERT INTO usuarios (nombre, passw) VALUES (:nombre, :passw)",
    #   {"nombre":nombre, "passw":passw} )
    #   return render_template("error.html", mensaje= "nuevo usuario creado")

    #return render_template("error.html", mensaje= "verificado")

@app.route("/hello/lector", methods=["POST"])
def lector():
    codigo = request.form.get("codigo")
    titulo = request.form.get("titulo")
    autor  = request.form.get("autor")

    if not codigo:
       codigo = "xxx" 
    if not titulo:
       titulo = "xxx"    
    if not autor:
       autor = "xxx"
    
    libros = db.execute("SELECT * FROM libros WHERE isbn LIKE ('%" + codigo + "%') OR titulo LIKE ('%" + titulo + "%') OR autor LIKE ('%" + autor + "%')").fetchall()
    
    if libros is not None:
       return render_template("libros.html", libros=libros)
 
#@app.route("/hello/lector/<int:libro_id>")
#def book(libro_id):
#    libro = db.execute("SELECT * FROM libros WHERE id = libro_id").fetchone()
#    return render_template("libro.html", libro=libro)  

    
