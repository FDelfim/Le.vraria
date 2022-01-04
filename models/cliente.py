class Cliente:

    def __init__(self, name, cpf, credit=0):
        self.__name = name
        self.__cpf = cpf
        self.__credit = credit

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @name.deleter
    def name(self):
        del self.name

    @property
    def cpf(self):
        return self.__cpf

    @cpf.setter
    def cpf(self, cpf):
        self.__cpf = cpf

    @cpf.deleter
    def cpf(self):
        del self.cpf

    @property
    def credit(self):
        return self.__credit

    @credit.setter
    def credit(self, credit):
        self.__credit = credit

    @credit.deleter
    def credit(self):
        del self.credit

    def sql_details(self):
        return f"('{self.name}', '{self.cpf}', '{self.credit}')"

    def __repr__(self):
        return "Cliente" + self.sql_details()
