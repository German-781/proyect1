import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    libros = db.execute("SELECT isbn, titulo, autor, año FROM libros").fetchall()
    for libro in libros:
        print(f"{libro.isbn}, {libro.titulo}, {libro.autor}, {libro.año}")

if __name__ == "__main__":
    main()
