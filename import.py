import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("libro2.csv")
    reader = csv.reader(f)
    for isbn, titulo, autor, año in reader:
        db.execute("INSERT INTO libros(isbn, titulo, autor, año) VALUES (:isbn, :titulo, :autor, :año)",
                   {"isbn": isbn, "titulo": titulo, "autor": autor, "año": año})
        print(f"Added libro from {isbn} to {autor} lasting {año}")
    db.commit()

if __name__ == "__main__":
    main()
