import sys
from enum import Enum

from datetime import datetime
from time import sleep, time

from io import StringIO

from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5.QtSql import QSqlQuery, QSqlDatabase

from lxml import etree as xml_helper
from src import canna_main


class Buchungstyp(Enum):
    Zugang = 1
    Abgang = 2
    Trocknung = 3
    Testung = 4

    def __str__(self):
        return self.name


class Kultivar(Enum):
    Sativa = 0
    Indica = 1
    Ruderalis = 2
    Hybrid = 3

    def __str__(self):
        return self.name


class Work(Enum):       # used to encode different types of work for database threading
    DB_Add = 0
    DB_Remove = 1
    XML_check = 2
    DB_check = 3
    # TODO add more work / thread types


class Buchung:
    pzn = "-0000000"
    type = Buchungstyp.Zugang
    time = None
    quantity = 0.0
    user = None
    batch = None
    wholesale_price = None
    expiry = None
    thc = None
    cbd = None
    kultivar = Kultivar.Sativa

    def __str__(self):
        return str(self.time) + " // " + str(self.type) + " (" + str(self.quantity) + "g)"


class Helper_Thread_new(QObject):
    # inspired by https://realpython.com/python-pyqt-qthread/

    finished = pyqtSignal()
    progress = pyqtSignal(int)

    work = []
    i = 0
    gui_master = None

    def run(self):
        """Long-running task."""
        while True: # TODO extend to "while running" oder so
            while len(self.work) > 0:
                print("thread has work to do: " + str(self.work[0][0]))
                if self.work[0][0] == Work.DB_Add:
                    # TODO implement all helper actions needed, e.g. add, remove, ...
                    print("ready to add :)")
                elif self.work[0][0] == Work.XML_check:
                    file = self.work[0][1]
                    schema = self.work[0][2]
                    self.gui_master.openAdmissionDialog()
                    # TODO move everything afterwards into this function


                elif self.work[0][0] == Work.DB_check:
                    self.check_db(self.work[0][1])

                self.progress.emit(self.i + 1)
                self.i += 1
                self.work.pop()
                print('some work done.')
                # sys.stdout.flush()
                sleep(1)
                #self.wait(1000)  # wait 1 sec

            print(".", end="")
            sleep(2)
            # self.wait(1000)

        self.finished.emit()


    def check_db(self, db_name):
        db_query = QSqlQuery()
        print("checking database . . . ", end='')
        db_con = QSqlDatabase.addDatabase("QSQLITE")
        db_con.setDatabaseName(db_name)
        if db_con.open():       # try to open
            print("database found. Opening . . . ", end="")
            if not db_con.tables().__contains__('test_table'):
                # create table if not already done
                if not db_query.exec("""
                            CREATE TABLE test_table (
                                id INTEGER PRIMARY KEY,
                                name VARCHAR(40) NOT NULL)
                            """):
                    print("database created. create table.")
                    # TODO create tables in database
                    #self.__init__(db_name, parent=parent)
            else:
                print("success. tables: ")
                print(db_con.tables())
        else:                   # fail while opening
            print("failed to open database.")


def check_xml(schema, file):
    print("checking xml . . . ", end="")
    try:
        test = StringIO(file)
        #tree = xml_helper.parse(StringIO(file))
        xml_file = xml_helper.parse(file)
        xml_validator = xml_helper.XMLSchema(file=schema)
        return xml_validator.validate(xml_file)

    except Exception as err:
        print("error!")
        print(err)
        return False


def read_xml(file):
    tree = xml_helper.parse(file)
    root = tree.getroot()
    admissions = []
    for child in root:
        # print(child.tag)
        temp = Buchung()
        for b in child:
            if b.tag == "pzn":
                temp.pzn = b.text
            elif b.tag == "quantity":
                temp.quantity = b.text
            elif b.tag == "type":
                temp.type = int(b.text)
            elif b.tag == "time":
                temp.time = b.text
        admissions.append(temp)
    return admissions


def find_list_index(list, index, isZugang):
    count_a = 0
    count_b = 0
    for i, l in enumerate(list):
        if l.type == Buchungstyp.Zugang:
            count_a += 1

        else:
            count_b += 1

        if count_a > index and isZugang:
            return i
        if count_b > index and not isZugang:
            return i


class Helper_Thread_old2(QThread):

    def __init__(self, db_name, parent=None):
        self.db_name = db_name
        self.db_query = QSqlQuery()
        self.work = []
        print("XX checking database . . . ", end='')
        self.db_con = QSqlDatabase.addDatabase("QSQLITE")
        self.db_con.setDatabaseName(db_name)
        if self.db_con.open():
            if not self.db_con.tables().__contains__('test_table'):
                # create table if not already done
                if not self.db_query.exec("""
                                CREATE TABLE test_table (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                                    name VARCHAR(40) NOT NULL)
                                """):
                    print("failed to create table.")
                    self.__init__(db_name, parent=parent)
            else:
                print("success. tables: ", end='')
                print(self.db_con.tables())
        else:
            print("failed to open database.")

        QThread.__init__(self, parent)
        self.started = True
        self.exiting = False

    def run(self):
        print("running?"+str(self.isRunning()))
        while self.started:
            while len(self.work) > 0:
                print("thread has work to do: " + str(self.work[0]))
                if self.work[0][0] == Work.Add:
                    # TODO implement all helper actions needed, e.g. add, remove, ...
                    print("ready to add :)")
                elif self.work[0][0] == Work.XML_check:
                    # TODO implement XML check from here
                    print("XXXXXXXX ready to check some XML in this thread..")

                self.work.pop()

                sys.stdout.write('..')
                #sys.stdout.flush()
                self.wait(1000) # wait 1 sec



class Helper_Thread_old(QThread):
    update_db = pyqtSignal()

    def __init__(self, db_name):
        self.db_name = db_name
        self.db_query = QSqlQuery()
        print("checking database . . . ", end='')
        self.db_con = QSqlDatabase.addDatabase("QSQLITE")
        self.db_con.setDatabaseName(db_name)
        if self.db_con.open():
            if not self.db_con.tables().__contains__('test_table'):
                # create table if not already done
                if not self.db_query.exec("""
                        CREATE TABLE test_table (
                            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                            name VARCHAR(40) NOT NULL)
                        """):
                    print("failed to create table.")
            else:
                print("success. tables: ", end='')
                print(self.db_con.tables())
        else:
            print("failed to open database.")

        QThread.__init__(self)

    def goon(self):
        try:
            self.keepgoing = True
            print("database-thread startet")
            self.start()
        except:
            print("database-thread stopped")
            self.pause()

    def add(self, content="123"):
        #global db_name, db_con
        print("adding database entry...", end='')
        query = QSqlQuery()
        print(query.exec(f"""INSERT INTO test_table (name) VALUES ('{content}')"""))
        sleep(1)
        print("done adding")

    def read_xml(self, file):
        tree = xml_helper.parse(file)
        # rough_string = xml_helper.tostring(tree)
        # print(rough_string)
        # result = xml_helper.fromstring(rough_string)
        # print(result)
        root = tree.getroot()
        buchungen = []
        for child in root:
            #print(child.tag)
            temp = Buchung()
            for b in child:
                if b.tag == "pzn":
                    temp.pzn = b.text
                elif b.tag == "quantity":
                    temp.quantity = b.text
                elif b.tag == "type":
                    temp.type = b.text
                elif b.tag == "time":
                    temp.time = b.text

                # print(b.tag, end=";")
                # print(b.text)

            buchungen.append(temp)
        return buchungen

    def check_xml(self, schema, file):
        try:
            xml_file = xml_helper.parse(file)
            xml_validator = xml_helper.XMLSchema(file=schema)
            return xml_validator.validate(xml_file)

        except Exception as err:
            print("error!")
            print(err)
            return False


    def remove(self, index):
        # TODO
        pass

    def select(self, index=-1):
        query = QSqlQuery()
        data = []
        if index == -1: # select ALL entries
            print(query.exec(f"""SELECT * FROM test_table"""))
            while query.next():
                data.append((query.value(0), query.value(1)))
                # print(query.value(0), query.value(1), query.value(2))
            return data
        else:           # select specific entry
            print(query.exec(f"""SELECT * FROM test_table WHERE id='{index}'"""))
            data.append((query.value(0), query.value(1)))

    def read_xml(self, file):
        tree = xml_helper.parse(file)
        # rough_string = xml_helper.tostring(tree)
        # print(rough_string)
        # result = xml_helper.fromstring(rough_string)
        # print(result)
        root = tree.getroot()
        buchungen = []
        for child in root:
            #print(child.tag)
            temp = Buchung()
            for b in child:
                if b.tag == "pzn":
                    temp.pzn = b.text
                elif b.tag == "quantity":
                    temp.quantity = float(b.text)
                elif b.tag == "type":
                    temp.type = Buchungstyp(int(b.text))
                elif b.tag == "time":
                    temp.time = datetime.strptime(b.text, '%Y-%m-%dT%H:%M:%S')

                # print(b.tag, end=";")
                # print(b.text)

            buchungen.append(temp)
        return buchungen

def main():
    file = "../xml/firstxml.xml"
    schema = "../xml/firstxsd.xsd"

    #print("checking...", end="")
    #print(Helper_Thread.check_xml(None, schema, file))
    #helper_thread.work.append(None)# TODO do xml check in thread

    print("reading...", end="")
    buchungen = Helper_Thread_old.read_xml(None, file)
    print(buchungen)


if __name__ == "__main__":
    main()
