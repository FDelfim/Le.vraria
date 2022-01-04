from database.connection import Database
from models.troca import Troca


class Trocas:
    def __init__(self):
        self.db = Database()
        self.dados = None

    def select(self, id_troca=None):
        self.db.open()
        if id_troca is None:
            self.db.cursor.execute("SELECT * FROM trocas")
        else:
            self.db.cursor.execute(
                f"SELECT * FROM trocas WHERE \"id_Troca\"={id_troca}")
        self.dados = self.db.cursor.fetchall()
        self.db.close()

    def insert(self, troca: Troca):
        self.db.open()
        insert_query = "INSERT INTO "\
            "trocas (\"id_Troca\", \"Livro_id\", \"Tier_livro\", cliente_id, data, funcionario_id) "\
            f"VALUES {troca.sql_details()}"
        self.db.cursor.execute(insert_query)
        self.db.update()
        self.db.close()

    def update(self, id_troca, data):
        self.db.open()
        update_query = f"UPDATE trocas SET data={data} WHERE \"id_Troca\"={id_troca}"
        self.db.cursor.execute(update_query)
        self.db.update()
        self.db.close()

    def delete(self, id_troca):
        self.db.open()
        delete_query = f"DELETE FROM trocas WHERE \"id_Troca\"={id_troca}"
        self.db.cursor.execute(delete_query)
        self.db.update()
        self.db.close()

    def count(self, id_troca=None):
        self.select(id_troca)
        return len(self.dados)

    def contains(self, id_troca=None):
        return self.count(id_troca) > 0
