from PyQt5 import QtCore
from ui.Confirmar_Exclusão import Ui_ConfirmarExclusao
from ui.adicionar_cliente import Ui_AdicionarCliente
from ui.main_menu import Ui_MainWindow
from pages.erro import Erro
from models.cliente import Cliente
from database.db_clientes import Clientes
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem


class ClientePage(Ui_MainWindow):
    def __init__(self, ui):
        self.ui = ui
        self.add = Adicionar()
        self.alt = Alterar()
        self.exc = Excluir()
        self.clientes = Clientes()
        self.buttons()

    def execute(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_creditos)
        self.table()

    def buttons(self):
        self.ui.pushButton_clientes_inserir.clicked.connect(self.inserir)
        self.ui.pushButton_clientes_alterar.clicked.connect(self.alterar)
        self.ui.pushButton_clientes_excluir.clicked.connect(self.excluir)
        self.ui.pushButton_consulta_2.pressed.connect(self.search)
        self.ui.lineEdit_consultacliente.returnPressed.connect(self.search)

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
        tabela = self.ui.tableWidget_Clientes
        tabela.setHorizontalHeaderLabels(
            ["NOME", "CPF", "CRÉDITOS"])

        tabela.setColumnWidth(0, 350)
        tabela.setColumnWidth(1, 400)
        tabela.setColumnWidth(2, 150)
        self.clientes.select()
        self.preencher_tabela(tabela, self.clientes.dados)

    def search(self):
        cpf = self.ui.lineEdit_consultacliente.text()
        self.ui.lineEdit_consultacliente.clear()
        if cpf == '':
            self.clientes.select()
            self.alt.clear()
            self.exc.clear()
        else:
            self.clientes.select(cpf)
            if self.clientes.contains(cpf):
                nome, cpf, creditos = self.clientes.dados[0]
                cliente = Cliente(nome, cpf, creditos)
                self.alt.cliente = cliente
                self.alt.load()
                self.exc.cliente = cliente
                self.exc.load()
        self.preencher_tabela(
            self.ui.tableWidget_Clientes, self.clientes.dados)

    def preencher_tabela(self, tabela: QTableWidget, itens):
        tabela.setRowCount(len(itens))
        for linha, item in enumerate(itens):
            for coluna, dado in enumerate(item):
                tabela.setItem(linha, coluna, QTableWidgetItem(str(dado)))


class Alterar(QMainWindow):

    def __init__(self, parent=None):
        super(Alterar, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.erro = Erro()
        self.alt = Ui_AdicionarCliente()
        self.clientes = Clientes()
        self.cliente = None
        self.alt.setupUi(self)
        self.buttons()
        self.set_text_window()

    def set_text_window(self):
        _translate = QtCore.QCoreApplication.translate
        self.alt.label_title.setText(
            _translate("MainWindow", "ALTERAR CLIENTE"))
        self.alt.pushButton_adicionar.setText(
            _translate("MainWindow", "ALTERAR"))

    def buttons(self):
        self.alt.pushButton_adicionar.clicked.connect(self.update)
        self.alt.pushButton_voltar.clicked.connect(self.close)

    def load(self):
        self.alt.lineEdit_1.setText(str(self.cliente.name))
        self.alt.lineEdit_2.setText(str(self.cliente.cpf))
        self.alt.lineEdit_3.setText(str(self.cliente.credit))

    def clear(self):
        self.alt.lineEdit_1.clear()
        self.alt.lineEdit_2.clear()
        self.alt.lineEdit_3.clear()

    def update(self):
        name = self.alt.lineEdit_1.text()
        cpf = self.alt.lineEdit_2.text()
        creditos = self.alt.lineEdit_3.text()

        if name != '' and cpf != '' and creditos != '':
            if self.checkCPF(cpf):
                cliente = Cliente(name, cpf, creditos)
                self.clientes.update(self.cliente.cpf, cliente)
                self.erro.execute("CLIENTE ALTERADO")
            else:
                self.erro.execute('CPF INVÁLIDO')

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
        self.cliente = None
        self.erro = Erro()

    def load(self):
        self.ui.label_2.setText("NOME: " + self.cliente.name +
                                "\nCPF: " + self.cliente.cpf +
                                "\nCRÉDITOS: " + str(self.cliente.credit))

    def clear(self):
        self.ui.label_2.setText("NOME: " +
                                "\nCPF: " +
                                "\nCRÉDITOS: ")

    def delete(self):
        clientes = Clientes()
        clientes.delete(self.cliente.cpf)
        self.erro.execute('CLIENTE EXCLUIDO COM SUCESSO')
        QtCore.QTimer.singleShot(2000, self.close)


class Adicionar(QMainWindow):

    def __init__(self, parent=None):
        super(Adicionar, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.clientes = Clientes()
        self.erro = Erro()
        self.add = Ui_AdicionarCliente()
        self.add.setupUi(self)
        self.buttons()

    def buttons(self):
        self.add.pushButton_adicionar.clicked.connect(self.finalizar)
        self.add.pushButton_voltar.clicked.connect(self.close)

    def finalizar(self):
        name = self.add.lineEdit_1.text()
        cpf = self.add.lineEdit_2.text()
        creditos = self.add.lineEdit_3.text()

        if name != '' and cpf != '' and creditos != '':
            if self.check_cpf(cpf):
                cliente = Cliente(name, cpf, creditos)
                self.clientes.insert(cliente)
                self.erro.execute("CLIENTE ADICIONADO")
            else:
                self.erro.execute('CPF INVÁLIDO')

        else:
            self.erro.execute()

    def check_cpf(self, cpf: str):
        if len(cpf) == 11:
            if cpf.isdigit():
                return True
        return False
