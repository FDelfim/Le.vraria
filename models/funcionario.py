class Funcionario:

    def __init__(self, name, password, cpf):
        self.__name = name
        self.__password = password
        self.__cpf = cpf

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
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        self.__password = password

    @password.deleter
    def password(self):
        del self.password

    @property
    def cpf(self):
        return self.__cpf

    @cpf.setter
    def cpf(self, cpf):
        self.__cpf = cpf

    @cpf.deleter
    def cpf(self):
        del self.cpf

    def __repr__(self):
        return "Funcionario" + self.sql_details()

    def sql_details(self):
        return f"('{self.name}', '{self.password}', '{self.cpf}')"
