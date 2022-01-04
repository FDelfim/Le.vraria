import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
from Files_Resource import loginImages
from database.db_funcionarios import Funcionarios
from menu import Application
from models.funcionario import Funcionario
from ui.loginUi import Ui_Login
from ui.cadastro import Ui_Cadastro


class Login(QMainWindow):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.user = None
        self.ui = Ui_Login()
        self.funcionarios = Funcionarios()
        self.funcionario = None
        self.ui.setupUi(self)
        self.disable_error()
        self.buttons()
        self.show()
        self.menu = Application
        self.cadastrar = Cadastro()

    def buttons(self):
        self.ui.pushButton_login.clicked.connect(self.login)
        self.ui.pushButton_cadastro.clicked.connect(self.cadastro_screen)
        self.ui.lineEdit_password.returnPressed.connect(self.login)

    def cadastro_screen(self):
        self.cadastrar.show()

    def checked_login(self):
        self.close()
        self.ui.lineEdit_password.clear()
        self.menu.show()
        self.menu.ui.pushButton_logout.clicked.connect(self.logout)

    def logout(self):
        self.ui.frame_error.setVisible(False)
        self.show()

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == QtCore.Qt.Key_Return:
            self.login()

    def login(self):
        user = self.ui.lineEdit_user.text()
        password = self.ui.lineEdit_password.text()
        auth = False
        self.funcionarios.select()
        for funcionario in self.funcionarios.dados:
            if user == funcionario[2] and password == funcionario[1]:
                auth = True
                self.user = funcionario[2]

        self.menu = Application(user=self.user)
        if auth:
            self.checked_login()
        else:
            self.enable_error()
            self.ui.label_error.setText("Usuário ou Senha Inválido(s)")
            self.ui.pushButton_close_error.clicked.connect(self.disable_error)

    def disable_error(self):
        self.ui.frame_error.setVisible(False)

    def enable_error(self):
        self.ui.frame_error.setVisible(True)
        QtCore.QTimer.singleShot(2000, self.disable_error)


class Cadastro(QMainWindow):
    def __init__(self, parent=None):
        super(Cadastro, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.ui = Ui_Cadastro()
        self.ui.setupUi(self)
        self.funcionarios = Funcionarios()
        self.disable_error()
        self.button()

    def button(self):
        self.ui.pushButton_cadastrar.clicked.connect(self.cadastrar)
        self.ui.pushButton_voltar.clicked.connect(self.voltar)

    def cadastrar(self):
        nome = self.ui.lineEdit_name.text()
        cpf = self.ui.lineEdit_cpf.text()
        password = self.ui.lineEdit_password.text()
        confirm_password = self.ui.lineEdit_confirmpassword.text()
        if confirm_password == password:
            funcionario = Funcionario(nome, password, cpf)
            self.funcionarios.insert(funcionario)

    def voltar(self):
        self.close()

    def disable_error(self):
        self.ui.frame_error.setVisible(False)

    def enable_error(self):
        self.ui.frame_error.setVisible(True)


def main():
    app = QApplication(sys.argv)
    login = Login()
    login.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
