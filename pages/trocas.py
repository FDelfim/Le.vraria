from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem
from database.db_clientes import Clientes
from database.db_livros import Livros
from database.db_troca import Trocas
from models.cliente import Cliente
from models.livro import Livro
from models.troca import Troca
from pages.erro import Erro
from ui.fazer_troca import Ui_FazerTroca
from ui.main_menu import Ui_MainWindow
from pages.erro import Erro
from models.cliente import Cliente


class TrocasPage(Ui_MainWindow):
    def __init__(self, ui, user=None):
        self.ui = ui
        self.user = user
        self.trocar = Trocar(user=self.user)
        self.livro = Livro
        self.livros = Livros()
        self.cliente = Cliente
        self.cliente = Clientes()
        self.trocas = Trocas()
        self.erro = Erro()
        self.buttons()

    def execute(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_trocas)
        self.table()

    def buttons(self):
        self.ui.pushButton_trocas_fazertroca.clicked.connect(self.inserir)
        self.ui.pushButton_consulta_trocas.pressed.connect(
            lambda: self.search())
        self.ui.lineEdit_consultatroca.returnPressed.connect(self.search)

    def inserir(self):
        self.trocar.show()

    def table(self):
        tabela = self.ui.tableWidget_Trocas
        tabela.setHorizontalHeaderLabels(
            ["ID TROCA", "ID LIVRO", "TIER", "CPF CLIENTE", "DATA TROCA", "CPF FUNCIONARIO"])

        tabela.setColumnWidth(0, 100)  # id troca
        tabela.setColumnWidth(1, 100)  # id livro
        tabela.setColumnWidth(2, 150)  # cpf cliente
        tabela.setColumnWidth(3, 250)  # cpf funcionario
        tabela.setColumnWidth(4, 100)  # tier livro
        tabela.setColumnWidth(5, 150)  # data troca

        self.trocas.select()
        self.preencher_tabela(tabela, self.trocas.dados)

    def search(self):
        id_troca = self.ui.lineEdit_consultatroca.text()
        if id_troca == '':
            self.trocas.select()
        else:
            if self.trocas.contains(id_troca):
                self.trocas.select(id_troca=id_troca)
            else:
                self.erro.execute("id troca não encontrado".upper())

        self.preencher_tabela(
            self.ui.tableWidget_Trocas, self.trocas.dados)
        self.ui.lineEdit_consultatroca.clear()

    def preencher_tabela(self, tabela: QTableWidget, itens):
        tabela.setRowCount(len(itens))
        for linha, item in enumerate(itens):
            for coluna, dado in enumerate(item):
                tabela.setItem(linha, coluna, QTableWidgetItem(str(dado)))


class Trocar(QMainWindow):

    def __init__(self, parent=None, user=None):
        super(Trocar, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.user = user
        self.cliente = None
        self.clientes = Clientes()
        self.livro = None
        self.livros = Livros()
        self.erro = Erro()
        self.troca = None
        self.trocas = Trocas()
        self.ui = Ui_FazerTroca()
        self.ui.setupUi(self)
        self.buttons()
        self.ui.lineEdit_3.setText(str(self.user))
        self.ui.lineEdit_3.setEnabled(False)

    def buttons(self):
        self.ui.pushButton_adicionar.pressed.connect(self.fazer_troca)
        self.ui.pushButton_voltar.clicked.connect(self.close)

    def fazer_troca(self):
        id_livro = self.ui.lineEdit_1.text()
        cpf_cliente = self.ui.lineEdit_2.text()

        if id_livro != '' and cpf_cliente != '':
            if self.clientes.contains(cpf_cliente):
                nome, cpf, creditos = self.clientes.dados[0]
                self.cliente = Cliente(nome, cpf, creditos)
                if self.livros.contains(id_livro):
                    id_book, title, author, tier, em_estoque = self.livros.dados[0]
                    if em_estoque:
                        self.livro = Livro(
                            id_book, title, author, tier=tier, em_estoque=em_estoque)
                        if int(self.cliente.credit) >= int(self.livro.tier) * 5:
                            self.efetuar_troca()
                        else:
                            self.erro.execute("CRÉDITOS INSUFICIENTES")
                    else:
                        self.erro.execute("Livro fora de estoque".upper())
                else:
                    self.erro.execute("LIVRO INEXISTENTE")
            else:
                self.erro.execute("CLIENTE INEXISTENTE")
        else:
            self.erro.execute()

    def efetuar_troca(self):
        id_troca = self.trocas.count()+1
        self.troca = Troca(id_troca, self.livro.id_livro,
                           self.cliente.cpf, self.user, self.livro.tier)
        self.trocas.insert(self.troca)
        self.cliente.credit = self.cliente.credit - (int(self.livro.tier) * 5)
        self.clientes.update(self.cliente.cpf, self.cliente)
        self.livro.em_estoque = False
        self.livros.update(self.livro.id_livro, self.livro)
        self.erro.execute("TROCA EFETUADA")
