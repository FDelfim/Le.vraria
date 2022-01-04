from ui.main_menu import Ui_MainWindow


class HomePage(Ui_MainWindow):
    def __init__(self, ui):
        self.ui = ui

    def execute(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
