from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Libro(db.Model):
    __tablename__ = "libros"
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String, nullable=False)
    titulo = db.Column(db.String, nullable=False)
    autor = db.Column(db.String, nullable=False)
    año = db.Column(db.Integer, nullable=False)

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    passw = db.Column(db.Integer, nullable=False)

class Comentario(db.Model):
    __tablename__ = "comentarios"
    id = db.Column(db.Integer, primary_key=True)
    coment = db.Column(db.String, nullable=False)
    nota = db.Column(db.Integer, nullable=False)
    num_rev = db.Column(db.Integer, nullable=True)
    score = db.Column(db.Integer, nullable=True)
    libro_id = db.Column(db.Integer, db.ForeignKey("libros.id"), nullable=False) 
    usu_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)   