from PyQt5 import QtCore
from database.db_clientes import Clientes
from database.db_livros import Livros
from models.cliente import Cliente
from models.livro import Livro
from ui.Confirmar_Exclusão import Ui_ConfirmarExclusao
from ui.adicionar_livro import Ui_AdicionarLivros
from ui.alterar_livro import Ui_AlterarLivro
from ui.main_menu import Ui_MainWindow
from pages.erro import Erro
from models.livro import Livro
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem


class LivrosPage(Ui_MainWindow):
    def __init__(self, ui):
        self.ui = ui
        self.add = Adicionar()
        self.alt = Alterar()
        self.exc = Excluir()
        self.erro = Erro()
        self.livros = Livros()
        self.buttons()

    def execute(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_livros)
        self.table()

    def buttons(self):
        self.ui.pushButton_livro_inserir.clicked.connect(self.inserir)
        self.ui.pushButton_livro_alterar.clicked.connect(self.alterar)
        self.ui.pushButton_livro_excluir.clicked.connect(self.excluir)
        self.ui.pushButton_consulta_livros.pressed.connect(
            lambda: self.search())
        self.ui.lineEdit_consulta_livros.returnPressed.connect(self.search)

    def inserir(self):
        self.exc.close()
        self.alt.close()
        self.add.show()

    def alterar(self):
        self.exc.close()
        self.add.close()
        self.alt.show()

    def excluir(self):
        self.alt.close()
        self.add.close()
        self.exc.show()

    def table(self):
        tabela = self.ui.tableWidget_livros
        tabela.setHorizontalHeaderLabels(
            ["ID", "TÍTULO", "AUTOR", "TIER", "EM ESTOQUE"])

        tabela.setColumnWidth(0, 50)
        tabela.setColumnWidth(1, 250)
        tabela.setColumnWidth(2, 350)
        tabela.setColumnWidth(3, 100)
        tabela.setColumnWidth(4, 100)
        self.livros.select()
        self.preencher_tabela(tabela, self.livros.dados)

    def search(self):
        id_livro = self.ui.lineEdit_consulta_livros.text()
        self.ui.lineEdit_consulta_livros.clear()
        if id_livro == '':
            self.livros.select()
            self.alt.clear()
            self.exc.clear()
        else:
            self.livros.select(id_livro)
            if self.livros.contains(id_livro):
                id_book, title, author, tier, em_estoque = self.livros.dados[0]
                livro = Livro(id_book, title, author,
                              tier=tier, em_estoque=em_estoque)
                print(livro)
                self.alt.livro = livro
                self.alt.load()
                self.exc.livro = livro
                self.exc.load()
        self.preencher_tabela(self.ui.tableWidget_livros, self.livros.dados)

    def preencher_tabela(self, tabela: QTableWidget, itens):
        tabela.setRowCount(len(itens))
        for linha, item in enumerate(itens):
            for coluna, dado in enumerate(item):
                tabela.setItem(linha, coluna, QTableWidgetItem(str(dado)))


class Adicionar(QMainWindow):
    def __init__(self, parent=None):
        super(Adicionar, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.livro = None
        self.erro = Erro()
        self.ui = Ui_AdicionarLivros()
        self.ui.setupUi(self)
        self.buttons()
        self.livros = Livros()

    def buttons(self):
        self.ui.pushButton_adicionar.clicked.connect(self.finalizar)
        self.ui.pushButton_voltar.clicked.connect(self.close)

    def finalizar(self):
        id_livro = self.livros.count() + 1
        titulo = self.ui.lineEdit_1.text()
        autor = self.ui.lineEdit_2.text()
        valor = self.ui.lineEdit_3.text()
        cpf_cliente = self.ui.lineEdit_5.text()
        if titulo != '' and autor != '' and valor != '':
            self.livro = Livro(id_livro, titulo, autor, valor)
            self.livros.insert(self.livro)
            self.erro.execute("LIVRO ADICIONADO")
        else:
            self.erro.execute('PREENCHA TODOS OS CAMPOS')
        if cpf_cliente != '':
            self.creditos(cpf_cliente)
        else:
            self.creditos()

    def creditos(self, cpf_cliente=0):
        clientes = Clientes()
        clientes.select(cpf_cliente)
        nome, cpf, creditos = clientes.dados[0]
        if int(cpf_cliente) != 0:
            creditos = int(creditos) + (int(self.livro.tier) * 10)
            self.erro.execute("CREDITOS GERADOS")
        cliente = Cliente(nome, cpf, creditos)
        clientes.update(cpf_cliente, cliente)


class Alterar(QMainWindow):
    def __init__(self, parent=None):
        super(Alterar, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.livros = Livros()
        self.livro = Livro
        self.erro = Erro()
        self.ui = Ui_AlterarLivro()
        self.ui.setupUi(self)
        self.buttons()

    def buttons(self):
        self.ui.pushButton_alterar.clicked.connect(self.update)
        self.ui.pushButton_voltar.clicked.connect(self.close)

    def load(self):
        self.ui.lineEdit_1.setText(str(self.livro.title))
        self.ui.lineEdit_2.setText(str(self.livro.author))
        self.ui.lineEdit_3.setText(str(self.livro.price))

    def clear(self):
        self.ui.lineEdit_1.clear()
        self.ui.lineEdit_2.clear()
        self.ui.lineEdit_3.clear()

    def update(self):
        titulo = self.ui.lineEdit_1.text()
        autor = self.ui.lineEdit_2.text()
        valor = self.ui.lineEdit_3.text()
        # id_cliente = self.ui.lineEdit_5.text()
        if titulo != '' and autor != '' and valor != '':
            livro = Livro(self.livro.id_livro, titulo, autor, valor)
            self.livros.update(self.livro.id_livro, livro)
            self.erro.execute('LIVRO ALTERADO COM SUCESSO')
        else:
            self.erro.execute()

    def checkCPF(self, cpf: str):
        if len(cpf) == 11:
            if cpf.isdigit():
                return True
        return False


class Excluir(QMainWindow):
    def __init__(self, parent=None):
        super(Excluir, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.ui = Ui_ConfirmarExclusao()
        self.ui.setupUi(self)
        self.ui.pushButton_cancelar.clicked.connect(self.close)
        self.ui.pushButton_excluir.clicked.connect(self.delete)
        self.livro = Livro
        self.erro = Erro()
        self.livros = Livros()

    def load(self):
        self.ui.label_2.setText("Id: " + str(self.livro.id_livro) + "\nTitulo: " +
                                self.livro.title + "\nAutor: " + self.livro.author)

    def clear(self):
        self.ui.label_2.setText("Id: " + "\nTitulo: " + "\nAutor: ")

    def delete(self):
        if self.livro.em_estoque:
            self.livros.delete(self.livro.id_livro)
            self.erro.execute('LIVRO EXCLUIDO COM SUCCESSO')
            QtCore.QTimer.singleShot(2000, self.close)
        else:
            self.erro.execute("Livro não pode ser deletado".upper())
