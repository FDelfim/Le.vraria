from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow
from ui.erro import Ui_Erro


class Erro(QMainWindow):
    def __init__(self, parent=None):
        super(Erro, self).__init__(parent)
        self.ui = Ui_Erro()
        self.ui.setupUi(self)

    def auto_close(self):
        QtCore.QTimer.singleShot(2000, self.close)

    def set_text(self, text: str):
        _translate = QtCore.QCoreApplication.translate
        self.ui.label.setText(_translate("MainWindow", text))

    def execute(self, text=None):
        if text is not None:
            self.set_text(str(text))
        self.show()
        self.auto_close()
