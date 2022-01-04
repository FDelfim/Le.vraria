from database.connection import Database
from models.cliente import Cliente


class Clientes:
    def __init__(self):
        self.db = Database()
        self.dados = None

    def select(self, cpf_cliente=None):
        self.db.open()
        if cpf_cliente is None:
            self.db.cursor.execute("SELECT * FROM clientes")
        else:
            self.db.cursor.execute(
                f"SELECT * FROM clientes WHERE \"cCPF\"='{cpf_cliente}'")
        self.dados = self.db.cursor.fetchall()
        self.db.close()

    def insert(self, cliente: Cliente):
        self.db.open()
        insert_query = "INSERT INTO clientes (\"cNome\", \"cCPF\", creditos) "\
            f"VALUES {cliente.sql_details()}"
        self.db.cursor.execute(insert_query)
        self.db.update()
        self.db.close()

    def update(self, cpf_cliente, cliente: Cliente):
        self.db.open()
        update_query = f"UPDATE clientes SET \"cNome\"='{cliente.name}', "\
            f"\"cCPF\"='{cliente.cpf}', creditos={cliente.credit} WHERE \"cCPF\"='{cpf_cliente}'"
        self.db.cursor.execute(update_query)
        self.db.update()
        self.db.close()

    def delete(self, cpf_cliente):
        self.db.open()
        delete_query = f"DELETE FROM clientes WHERE \"cCPF\"='{cpf_cliente}'"
        self.db.cursor.execute(delete_query)
        self.db.update()
        self.db.close()

    def count(self, cpf_cliente=None):
        self.select(cpf_cliente)
        return len(self.dados)

    def contains(self, cpf_cliente=None):
        self.count(cpf_cliente)
        return len(self.dados) > 0
