import time

from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtSql import QSqlQuery
import sys

from PyQt5.QtWidgets import QDialog, QMessageBox

from src import XML_DB_helper as data_helper
from gui import main_window, admission_mask

from PyQt5 import QtWidgets
from PyQt5.QtCore import QModelIndex, Qt, QAbstractTableModel, QItemSelectionModel, QDate, QThread

"""
2Dos:
- Passwortgeschützte Datenbank
- 
"""


class GUI(main_window.Ui_MainWindow, QtWidgets.QMainWindow):

    def __init__(self):
        super(GUI, self).__init__()
        self.setupUi(self)
        self.tuneUi()       # custom changes on GUI

    def treeUpdate(self):
        a = self.treeWidget.currentIndex()
        print("tree update!@"+str(a))


    def tuneUi(self):
        # set icon
        self.setWindowIcon(QIcon("../res/mainicon.png"))
        import ctypes
        myappid = u'mycompany.myproduct.subproduct.version'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        # treeView adjustment
        for c in range(self.treeWidget.columnCount()):
            print("resizing column #"+ str(c))
            self.treeWidget.resizeColumnToContents(c)

        # columnView adjustment
        #model = QStandardItemModel()
        #model.setColumnCount(2)
        #self.columnView.setModel(model)

        # connect selection-changed-trigger
        #selection_model = self.columnView.selectionModel()
        #selection_model.selectionChanged.connect(self.colViewChanged)
        #self.columnView.selectionModel = selection_model
        #self.columnView.selectionModel.selectionChanged.connect(self.colViewChanged())

        # columnView exemplary content
        """
        s_a = QStandardItem("Sorte A")
        s_b = QStandardItem("Sorte B")
        s_c = QStandardItem("Sorte C")
        model.appendRow(s_a)
        model.appendRow(s_b)
        model.appendRow(s_c)
        c_a = QStandardItem("Charge A")
        c_b = QStandardItem("Charge B")
        s_a.appendRow(c_a)
        s_a.appendRow(c_b)
        p_a = QStandardItem("PZN 123 (5g)")
        p_b = QStandardItem("PZN 456 (10g)")
        p_c = QStandardItem("PZN 789 (15g)")
        c_a.appendRow(p_a)
        c_a.appendRow(p_b)
        c_a.appendRow(p_c)
        """


    def colViewChanged(self):
        print("colViewChanged! TODO: update Sorten Infos & Chargen Infos")
        # TODO indeci herausfinden, die ausgewählt wurden
        index = self.columnView.selectionModel().currentIndex()
        print("index: "+str(index.row())+ " : "
              + str(index.column()))
        print(":)")

        if index.row() == 0:
            self.label_2.setText("23,5g")

        else:
            self.label_2.setText("1,0g")
        #index = self.columnView.selectedIndexes()


    def add(self):
        print("adding...")
        helper_thread.add(content='test123')
        self.update_table()

    def replenishment(self):
        print("Neuer Zugang!")
        # TODO fill with life

    def dispatchment(self):
        print("Neuer Abgang!")
        # TODO fill with life

    def new_order(self):
        print("Neuer Auftrag!")
        # TODO fill with life

    def shopping_advice(self):
        print("Einkaufsempfehlung!")
        # TODO fill with life

    def remove(self):
        # TODO
        self.update_table(all=False)

    def add_to_table(self, entries, table):
        old_rows = table.rowCount()
        table.setRowCount(old_rows + len(entries))
        print("adding to table:")
        for index, entry in enumerate(entries):
            print(index, entry)
            table.setItem(old_rows + index, 0, QtWidgets.QTableWidgetItem(str(entry.time)))
            table.setItem(old_rows + index, 1, QtWidgets.QTableWidgetItem(str(entry.type)))
            table.setItem(old_rows + index, 2, QtWidgets.QTableWidgetItem(str(entry.pzn)))
            table.setItem(old_rows + index, 3, QtWidgets.QTableWidgetItem(str(entry.quantity)))

    def admission_review(self, gui, admissions):
        dlg = AdmissionDlg(admissions)
        dlg.setWindowTitle("Neue Buchungen")
        if dlg.exec():
            print("zurück im hauptmenu")
            # TODO checken, ob änderungen auch hier in admissions angekommen sind
            #self.add_to_table(admissions, self.tableWidget_3)

            # TODO save data from admissions to database
            # TODO calculate new stock from those new admissions
            # TODO clear xml from Zugänge
        else:
            print("something went wrong // no admissions will be integrated into database")

    def xml_check(self):
        file = "xml/firstxml.xml"
        schema = "xml/firstxsd.xsd"

        # remove, da nicht mehr vom thread erledigt:
        # worker.work.append((data_helper.Work.XML_check, file, schema))
        # TODO alternative, sequenziell (kein Thread) hier die buchungen auslesen
        if data_helper.check_xml(schema, file):
            print("ok")
            print("reading xml  . . . ", end="")
            buchungen = data_helper.read_xml(file)
            print("ok")

            admissions = []     # admissions = zugänge
            for b in buchungen:
                if data_helper.Buchungstyp(b.type) == data_helper.Buchungstyp.Zugang:
                    admissions.append(b)
            if len(admissions) > 0:
                try:
                    self.admission_review(self, buchungen)
                    # TODO instead of calling: emmit signal (2BD)
                    # TODO not self.admission_review(buchungen)
                except Exception as e:
                    print(e)
            else:
                print("no bookings in XML!")
                # TODO show_message_box("Keine Buchungen verfügbar.", "Keine Buchungen")

        else:
            print("xml is not in valid format")
            # TODO show_message_box("Fehler beim Auslesen der XML-Datei.", "XML-Fehler")

    def update_table(self, all=True, index=None):
        if all: data = helper_thread.select()
        else: data = helper_thread.select(index)

        #self.ui.tableWidget.setRowCount(len(data))

        for row_i, row in enumerate(data):
            # print (index, row)
            # print("test")
            self.tableWidget.setItem(row_i, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.tableWidget.setItem(row_i, 1, QtWidgets.QTableWidgetItem(row[1]))

        print("table content updated")
        self.tableWidget.viewport().update()

        #model = MyTableModel(data)
        #self.tableView.setModel(model)
        #self.tableView.show()

        #self.pushButton.setText("newtext")


class AdmissionDlg(QDialog):
    def __init__(self, admissions, parent=None):
        super().__init__(parent)
        self.admissions = admissions
        # used to save entered values on the run
        self.old_index_t0 = -1  # index in tab 0
        self.old_index_t1 = -1  # index in tab 1

        # Create an instance of the GUI
        self.ui = admission_mask.Ui_Dialog()
        # Run the .setupUi() method to show the GUI
        self.ui.setupUi(self)
        self.tuneUi(admissions)

    def tuneUi(self, admissions):
        # set icon
        self.setWindowIcon(QIcon("../res/stockicon.png"))
        import ctypes
        myappid = u'mycompany.myproduct.subproduct.version'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        # fill with passed admissions
        model = QStandardItemModel()
        model2 = QStandardItemModel()
        self.ui.listView.setModel(model)
        self.ui.listView_2.setModel(model2)

        for i, a in enumerate(admissions):
            item = QStandardItem(str(a))
            try:
                if data_helper.Buchungstyp(a.type) == data_helper.Buchungstyp.Zugang:
                    model.appendRow(item)
                else:
                    model2.appendRow(item)
            except Exception as e:
                print(e)

        ix = model.index(0, 0)
        sm = self.ui.listView.selectionModel()
        sm.select(ix, QItemSelectionModel.Select)
        #self.index_changed()

        # connect with slot
        self.ui.listView.selectionModel().selectionChanged.connect(self.index_changed)
        self.ui.listView_2.selectionModel().selectionChanged.connect(self.index_changed)
        #self.ui.listView.setCurrentIndex(QModelIndex(0, 0))

    def check_exit(self):
        print("checking input... ")
        # TODO funktion wieder aktiveren - derzeit prüft sie nicht wirklich (debugging)
        for i, a in enumerate(self.admissions):
            if i == self.ui.listView.selectionModel().currentIndex().row(): continue
            if a.batch is None or a.batch == "" or a.wholesale_price is None or a.user is None or a.expiry is None:
                print("aaa missing input for admission #"+str(i))
                show_message_box("Bitte überprüfen Sie eingebenen\nDaten auf Vollständigkeit!", "Fehlerhafte Daten")
                #return # TODO

        if self.ui.lineEdit.text() == "" or self.ui.dateEdit.date() == QDate(2000, 1, 1) \
            or self.ui.comboBox.currentIndex() == -1 or self.ui.doubleSpinBox.value() == 0:
            print("bbb missing input for admission #" + str(self.ui.listView.currentIndex().row()))
            show_message_box("Bitte überprüfen Sie eingebenen\nDaten auf Vollständigkeit!", "Fehlerhafte Daten")
        #else: # TODO
            if show_message_box("Möchten Sie die " + str(len(self.admissions)) + " Buchungen\nin die Datenbank "
                    "übernehmen?", "Speichern in Datenbank", QMessageBox.Question, buttons=QMessageBox.Yes |
                                                                                    QMessageBox.No) == QMessageBox.Yes:
                self.accept()

    def tab_changed(self):
        self.index_changed()

    def index_changed(self):
        tab = self.ui.tabWidget.currentIndex()
        if tab == 0:
            #old_index = self.old_index_t0
            old_index = find_list_index(self.admissions, self.old_index_t0, True)
        else:
            #old_index = self.old_index_t1
            old_index = find_list_index(self.admissions, self.old_index_t1, False)

        print ("super check 1")

        if old_index != -1:
            # save old values
            self.admissions[old_index].batch = self.ui.lineEdit.text()
            self.admissions[old_index].user = self.ui.comboBox.currentText()
            self.admissions[old_index].wholesale_price = self.ui.doubleSpinBox.value()
            self.admissions[old_index].expiry = self.ui.dateEdit.date()
            self.admissions[old_index].thc = self.ui.spinBox.value()
            self.admissions[old_index].cbd = self.ui.spinBox_2.value()
            self.admissions[old_index].kultivar = data_helper.Kultivar(self.ui.comboBox_2.currentIndex())

        print("super check 2")

        if tab == 0:
            i = self.ui.listView.currentIndex().row()
            if i == -1:
                i = 0
            self.old_index_t0 = i #find_list_index(self.admissions, i, True)
        else:
            i = self.ui.listView_2.currentIndex().row()
            if i == -1:
                i = 0
            self.old_index_t1 = i #find_list_index(self.admissions, i, False)

        ## TODO implement saving, temporary saving and updating information fields when changing admissions

        # TODO find corresponding admission, i is currently misleading

        # update information on booking at new selection
        j = find_list_index(self.admissions, i, tab == 0)
        try:
            self.ui.label_4.setText(str(self.admissions[j].time))
            self.ui.label_5.setText(str(self.admissions[j].type))
            self.ui.label_6.setText(self.admissions[j].pzn)
            self.ui.label_8.setText(str(self.admissions[j].quantity) + " g")
            # TODO fill the rest thc cbd kultivar
            if self.admissions[j].batch is not None:                        # charge
                self.ui.lineEdit.setText(self.admissions[j].batch)
            else:
                self.ui.lineEdit.setText("")
            if self.admissions[j].kultivar is not None:                     # kultivar
                self.ui.comboBox_2.setCurrentText(str(self.admissions[j].kultivar))
            else:
                self.ui.comboBox_2.clear()
            if self.admissions[j].thc is not None:                          # thc
                self.ui.spinBox.setValue(self.admissions[j].thc)
            else:
                self.ui.spinBox.clear()
            if self.admissions[j].cbd is not None:                         # cbd
                self.ui.spinBox_2.setValue(self.admissions[j].cbd)
            else:
                self.ui.spinBox_2.clear()
            if self.admissions[j].expiry is not None:                       # expiry
                self.ui.dateEdit.setDate(self.admissions[j].expiry)
            else:
                self.ui.dateEdit.clear()
            if self.admissions[j].user is not None:                         # user
                self.ui.comboBox.setCurrentText(self.admissions[j].user)
            else:
                self.ui.comboBox.clear()
            if self.admissions[j].wholesale_price is not None:              # wholesale price
                self.ui.doubleSpinBox.setValue(self.admissions[j].wholesale_price)
            else:
                self.ui.doubleSpinBox.clear()

        except Exception as e:
            print(e)


def find_list_index(list, index, isZugang):
    count_a = 0
    count_b = 0
    for i, l in enumerate(list):
        if l.type == data_helper.Buchungstyp.Zugang:
            count_a += 1

        else:
            count_b += 1

        if count_a > index and isZugang:
            return i
        if count_b > index and not isZugang:
            return i


def show_message_box(message, title, icon=QMessageBox.Warning, buttons=QMessageBox.Ok):
    msg = QMessageBox()
    msg.setIcon(icon)
    msg.setText(message)
    msg.setWindowTitle(title)
    msg.setStandardButtons(buttons)
    return msg.exec_()


class MyTableModel(QAbstractTableModel):
    def __init__(self, data=[[]], parent=None):
        super().__init__(parent)
        self.data = data

    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return "Column " + str(section)
            else:
                return "Row " + str(section)

    def columnCount(self, parent=None):
        return len(self.data[0])

    def rowCount(self, parent=None):
        return len(self.data)

    def data(self, index: QModelIndex, role: int):
        if role == Qt.DisplayRole:
            row = index.row()
            col = index.column()
            return str(self.data[row][col])


def db_delete_entry():
    # TODO
    print("removing database entry...")
    createTableQuery = QSqlQuery()
    createTableQuery.exec(
        """
        CREATE TABLE contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            name VARCHAR(40) NOT NULL,
            job VARCHAR(50),
            email VARCHAR(40) NOT NULL
        )
        """)


def db_get_entry():
    # TODO
    print("getting database data...")


def thread_starter():
    # Step 2: Create a QThread object
    thread = QThread()
    # Step 3: Create a worker object
    worker = data_helper.Helper_Thread_new()
    # Step 4: Move worker to the thread
    worker.moveToThread(thread)
    # Step 5: Connect signals and slots
    thread.started.connect(worker.run)
    # TODO define new slot where worker is finished with new admission (newadmissions) ->
    # TODO connect with admission_review
    worker.finished.connect(thread.quit)
    worker.finished.connect(worker.deleteLater)
    thread.finished.connect(thread.deleteLater)
    # Step 6: Start the thread
    thread.start()
    return thread, worker


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = GUI()

    # database thread so QT does not interfere with database access
    global helper_thread, db_name, worker
    helper_thread, worker = thread_starter()
    helper_thread.master_gui = window

    # TODO direkt die DB checken
    db_name = "data2.db"
    worker.work.append((data_helper.Work.DB_check, db_name))

    #helper_thread = data_helper.Helper_Thread(db_name)
    #helper_thread.run()
    #print("is now running?"+str(helper_thread.isRunning()))

    # connect signals
    # TODO

    # window.update_table()
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
