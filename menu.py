from PyQt5.QtWidgets import QMainWindow
from pages.clientes import ClientePage
from pages.home import HomePage
from pages.livros import LivrosPage
from pages.trocas import TrocasPage
from ui.main_menu import Ui_MainWindow


class Application(QMainWindow):
    def __init__(self, parent=None, user=None):
        super(Application, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.user = user
        self.home_page = HomePage(self.ui)
        self.livros_page = LivrosPage(self.ui)
        self.cliente_page = ClientePage(self.ui)
        self.trocas_page = TrocasPage(self.ui, self.user)
        self.default_page()
        self.mainwin()

    def default_page(self):
        self.home_page.execute()

    def mainwin(self):
        self.ui.pushButton_home.clicked.connect(
            lambda: HomePage(self.ui))
        self.ui.pushButton_livros.clicked.connect(
            self.livros_page.execute)
        self.ui.pushButton_creditos.clicked.connect(
            self.cliente_page.execute)
        self.ui.pushButton_trocas.clicked.connect(
            self.trocas_page.execute)
        self.ui.pushButton_logout.clicked.connect(self.close)


def main():
    import sys
    from PyQt5.QtWidgets import QApplication
    from Files_Resource import loginImages
    app = QApplication(sys.argv)
    application = Application()
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
