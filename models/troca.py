class Troca:
    def __init__(self, id_troca, id_livro, cpf_cliente, cpf_funcionario, tier_livro):
        self.id_troca = id_troca
        self.id_livro = id_livro
        self.cpf_cliente = cpf_cliente
        self.cpf_funcionario = cpf_funcionario
        self.tier_livro = tier_livro
        self.data = 'today'

    def nota_fiscal(self):
        nota = "id_troca: " + str(self.id_troca) + \
            ", id_livro: " + str(self.id_livro) + \
            ", cpf_cliente: " + str(self.cpf_cliente) + \
            ", cpf_funcionario: " + str(self.cpf_funcionario) + \
            ", tier: " + str(self.tier_livro) + \
            ", data troca: " + str(self.data)
        return nota

    def sql_details(self):
        details = f"({self.id_troca}, " + \
                  f"{self.id_livro}, " + \
                  f"{self.tier_livro}, " + \
                  f"'{self.cpf_cliente}', " + \
                  f"'{self.data}', " + \
            f"'{self.cpf_funcionario}')"
        return details
