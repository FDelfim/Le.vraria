from database.connection import Database
from models.funcionario import Funcionario


class Funcionarios:

    def __init__(self):
        self.db = Database()
        self.dados = None

    def select(self, cpf_funcionario=None):
        self.db.open()
        if cpf_funcionario is None:
            self.db.cursor.execute("SELECT * FROM funcionarios")
        else:
            self.db.cursor.execute(
                f"SELECT * FROM funcionarios WHERE \"fCPF\"='{cpf_funcionario}'")
        self.dados = self.db.cursor.fetchall()
        self.db.close()

    def insert(self, funcionario: Funcionario):
        self.db.open()
        insert_query = "INSERT INTO funcionarios "\
            "(\"id_Funcionario\", \"fNome\", \"fSenha\", \"fCPF\") "\
            f"VALUES {funcionario.sql_details()}"
        self.db.cursor.execute(insert_query)
        self.db.update()
        self.db.close()

    def update(self, cpf_funcionario, nova_senha):
        self.db.open()
        update_query = "UPDATE funcionarios "\
            f"SET \"fsenha\": {nova_senha} "\
            f"WHERE \"fCPF\"={cpf_funcionario}"
        self.db.cursor.execute(update_query)
        self.db.update()
        self.db.close()

    def delete(self, cpf_funcionario):
        self.db.open()
        delete_query = "DELETE FROM funcionarios "\
            f"WHERE \"fCPF\"={cpf_funcionario}"
        self.db.cursor.execute(delete_query)
        self.db.update()
        self.db.close()

    def count(self):
        self.select()
        return len(self.dados)
