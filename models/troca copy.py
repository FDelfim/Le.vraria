from datetime import date

from cliente import Cliente
from funcionario import Funcionario
from livro import Livro


class Trocas:
    def __init__(self, id_troca, cliente: Cliente, funcionario: Funcionario, livro: Cliente):
        self.id_troca = id_troca
        self.data = today_date()
        self.cliente = cliente
        self.funcionario = funcionario
        self.livro = livro

    def nota_fiscal(self):
        nota = "id_troca: " + str(self.id_troca) + \
            ", data: " + self.data + \
            ", id_cliente: " + str(self.cliente.id_cliente) + \
            ", id_funcionario: " + str(self.funcionario.id_funcionario) + \
            ", livro: " + self.livro.title + \
            ", tier: " + str(self.livro.tier)
        return nota

    def sql_details(self):
        details = f"('{self.id_troca}', " + \
                  f"'{self.data}', " + \
                  f"'{self.cliente.id_cliente}', " + \
                  f"'{self.funcionario.id_funcionario}', " + \
                  f"'{self.livro.id_livro}')"
        return details
