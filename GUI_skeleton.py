import sys
import some_QtGUI_file
from PyQt5 import QtWidgets


class GUI(some_QtGUI_file.Ui_MainWindow, QtWidgets.QMainWindow):

    def __init__(self):
        super(GUI, self).__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = GUI()
    window.show()
    sys.exit(app.exec())
