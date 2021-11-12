import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow
# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import MenuBar
import clickme
import untitled


class testGUI(untitled.Ui_MainWindow, QMainWindow):

    def __init__(self):
        super(testGUI, self).__init__()
        self.setupUi(self)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Strg+F8 to toggle the breakpoint.


def qt_test():
    # Create the application object
    app = QtWidgets.QApplication(sys.argv)

    # directly create the form object
    # first_window = QtWidgets.QWidget()
    # Create window from UI defined in untitled.py
    first_window = testGUI()

    # Set window size
    #first_window.resize(400, 300)

    # Set the form title
    #first_window.setWindowTitle("The first pyqt program")

    # Show form
    first_window.show()

    # Run the program
    sys.exit(app.exec())



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
def print_hallowelt():
    print("Hallo Welt")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    print_hallowelt()
    qt_test()






