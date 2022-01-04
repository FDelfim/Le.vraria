class Livro:

    def __init__(self, id_livro, title, author, price=None, tier=None, em_estoque=True):
        self.__id_livro = id_livro
        self.__title = title
        self.__author = author
        self.__price = price
        self.__tier = tier
        self.em_estoque = em_estoque
        self.set_tier()

    @property
    def id_livro(self):
        return self.__id_livro

    @id_livro.setter
    def id_livro(self, id_livro):
        self.__id_livro = id_livro

    @id_livro.deleter
    def id_livro(self):
        del self.__id_livro

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = title

    @title.deleter
    def title(self):
        del self.title

    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self, author):
        self.__author = author

    @author.deleter
    def author(self):
        del self.__author

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, price):
        self.__price = price

    @price.deleter
    def price(self):
        del self.__price

    @property
    def tier(self):
        return self.__tier

    @tier.setter
    def tier(self, tier):
        self.__tier = tier

    @tier.deleter
    def tier(self):
        del self.__tier

    def set_tier(self):
        if self.tier is None:
            price = float(self.price) * 0.8
            if price > 49:
                self.tier = 3
            if 20 < price <= 50:
                self.tier = 2
            if price <= 20:
                self.tier = 1

    def sql_details(self):
        dados = f"('{self.id_livro}', "\
            f"'{self.title}', "\
            f"'{self.author}', "\
            f"'{self.tier}',"\
            f"{self.em_estoque})"
        return dados

    def __repr__(self):
        return "Livro" + self.sql_details()
