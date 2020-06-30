import os

from models import *

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from flask import Flask, render_template, request, session, redirect

app = Flask(__name__)
app.secret_key = 'mi clave secreta'

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    nombre = ''
    passw = ''
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    nombre = request.form.get("nombre")
    passw = request.form.get("passw")
    
    try:
       passw = int(passw)
    except ValueError:     
       return render_template("error.html", mensaje= "password debe ser numerica")

    usuario = db.execute("SELECT * FROM usuarios WHERE nombre = ('" + nombre + "')").first()
    if usuario is None:
      db.execute("INSERT INTO usuarios (nombre, passw) VALUES (:nombre, :passw)",
      {"nombre":nombre, "passw":passw} )

      db.commit()

      return render_template("error.html", mensaje= "nuevo usuario creado")

    passw=str(passw)
    user = db.execute("SELECT * FROM usuarios WHERE nombre = ('" + nombre + "') AND passw = ('" + passw + "')").first()
    if user is None:
       return render_template("error.html", mensaje= "password no corresponde")

    session['logged_in'] = True   
    session['usuario_id'] = user.id 
    
    return render_template("login.html")
 
@app.route("/lector", methods=["POST"])
def lector():
    session['codigo'] = request.form.get("codigo")
    session['titulo'] = request.form.get("titulo")
    session['autor']  = request.form.get("autor")

    return redirect('/libros')

@app.route("/libros")
def libros():
   
    if 'codigo' in session:
      codigo = session['codigo']
    if 'titulo' in session:
      titulo = session['titulo']
    if 'autor' in session:
      autor = session['autor']   

    if not codigo:
       codigo = "xxx" 
    if not titulo:
       titulo = "xxx"    
    if not autor:
       autor = "xxx"
  

    libros = db.execute("SELECT * FROM libros WHERE isbn LIKE ('%" + codigo + "%') OR titulo LIKE ('%" + titulo + "%') OR autor LIKE ('%" + autor + "%')").fetchall()
    
    if libros is not None:
       return render_template("libros.html", libros=libros)
 
@app.route("/libros/<int:libro_id>")  
def libro(libro_id):

    session['libro_id'] = libro_id

    libro = db.execute("SELECT * FROM libros WHERE id = '%s'"%libro_id).fetchone()

    isbn = libro.isbn

   #accesa API de Goodreads
    import requests
    base = "isbn"
    res=requests.get("https://www.goodreads.com/book/review_counts.json",params={"key":"uYFyo76mrXdoDZ658eU1Q","isbns":"0812995341"})


    print(res.json())

    if 'usuario_id' in session:
       usuario_id = session['usuario_id']
       print(usuario_id) 
    print("GGerman")   

    usua_id = str(usuario_id)
    libra_id = str(libro_id)
    comentario = db.execute("SELECT * FROM comentarios WHERE usu_id = ('" + usua_id + "') AND libro_id  = ('"+ libra_id +"')").first()


    if comentario is None:
       comentarios = 'no hay comentarios'
       return render_template("libro.html", libro=libro, comentario=comentario) 
    return render_template("libro.html", libro=libro, comentario=comentario) 


@app.route("/califica", methods=["POST"])
def califica():    
    nota = request.form.get("nota")
    coment = request.form.get("coment")
    if 'usuario_id' in session:
       usu_id = session['usuario_id']
    if 'libro_id' in session:
       libro_id = session['libro_id']

    num_rev = 0
    score = 0
    usua_id = str(usu_id)
    libra_id = str(libro_id)
    exist = db.execute("SELECT * FROM comentarios WHERE usu_id = ('" + usua_id + "') AND libro_id  = ('"+ libra_id +"')").first()

    if exist is not None:
       print("ya existe")
    #   return render_template("logout.html", mensaje= "libro ya calificado") 
       mensaje = "comentario ya ingresado"
    #  return render_template("logout.html")
       session['mensaje'] = mensaje
       return redirect('/logout')

    db.execute("INSERT INTO comentarios (coment, nota, num_rev, score, libro_id, usu_id) VALUES (:coment, :nota, :num_rev, :score, :libro_id, :usu_id)",
    {"coment":coment, "nota":nota, "num_rev":num_rev, "score":score, "libro_id":libro_id, "usu_id":usu_id})

    db.commit()       
    
    mensaje = "comentario ingresado"
    session['mensaje'] = mensaje

    return redirect('/logout')

@app.route('/logout')
def logout():

    if 'mensaje' in session:
       mensaje = session['mensaje']

    return render_template("logout.html",mensaje=mensaje)

    session['logged_in'] = False

