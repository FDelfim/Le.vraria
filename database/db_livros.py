from database.connection import Database
from models.livro import Livro


class Livros:
    def __init__(self):
        self.db = Database()
        self.dados = None

    def select(self, id_livro=None):
        self.db.open()
        if id_livro is None:
            self.db.cursor.execute("SELECT * FROM livros")
        else:
            self.db.cursor.execute(
                f"SELECT * FROM livros WHERE id_livro={id_livro}")
        self.dados = self.db.cursor.fetchall()
        self.db.close()

    def insert(self, livro: Livro):
        self.db.open()
        insert_query = "INSERT INTO "\
            "livros (id_livro, titulo, autor, tier, em_estoque) "\
            f"VALUES {livro.sql_details()}"
        self.db.cursor.execute(insert_query)
        self.db.update()
        self.db.close()

    def update(self, id_livro, livro: Livro):
        self.db.open()
        update_query = f"UPDATE livros SET id_livro={livro.id_livro}, titulo='{livro.title}', autor='{livro.author}', tier={livro.tier}, em_estoque={livro.em_estoque} WHERE id_livro={id_livro}"
        self.db.cursor.execute(update_query)
        self.db.update()
        self.db.close()

    def delete(self, id_livro):
        self.db.open()
        delete_query = f"DELETE FROM livros WHERE id_livro={id_livro}"
        self.db.cursor.execute(delete_query)
        self.db.update()
        self.db.close()

    def count(self, id_livro=None):
        self.select(id_livro)
        return len(self.dados)

    def contains(self, id_livro=None):
        self.count(id_livro)
        return len(self.dados) > 0
