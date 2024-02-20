# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton, QMessageBox
from PySide6.QtTest import QTest
from PySide6.QtCore import QTimer
from ui_form import Ui_MainWindow
import json
import ping_func

# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.tabs=self.ui.tabWidget
        self.check=self.ui.checkBox
        self.check.stateChanged.connect(self.change)
        self.spin=self.ui.spinBox
        self.spin.valueChanged.connect(self.change)
        self.button=self.ui.pushButton
        self.button.clicked.connect(self.event_button)
        self.searchButton=self.ui.searchButton
        self.searchButton.clicked.connect(self.eventSearch)
        self.searchText=self.ui.searchText
        self.action()
        self.timer=QTimer(self)
        self.timer.timeout.connect(self.update_ping)
        self.change()

    def action(self):
        '''self.tab1=QWidget()
        self.tab2=QWidget()
        self.tabs.addTab(self.tab1,"СПФ А")
        self.tabs.addTab(self.tab2,"СПФ Б")
        self.tab1.layout=QVBoxLayout(self)
        self.tab1.layout.layoutH=QHBoxLayout(self)
        self.tab2.layout=QVBoxLayout(self)
        self.l=QLabel()
        self.l.setText("Кто - то")
        self.ll=QLabel()
        self.ll.setText("То - то")
        self.lll=QLineEdit()
        self.lll.setText("123")
        self.lll.setEnabled(False)
        self.tab1.layout.layoutH.addWidget(self.l)
        self.tab1.layout.layoutH.addWidget(self.ll)
        self.tab1.layout.layoutH.addWidget(self.lll)
        self.tab1.setLayout(self.tab1.layout)
        self.tab1.layout.addLayout(self.tab1.layout.layoutH)
        self.tab1.layout.addStretch(0)'''
        self.check.setEnabled(False)
        self.spin.setEnabled(False)
        self.tab=[]
        self.tab_ip=[]
        self.tab_names=[]
        self.labels_status=[]
        self.vertical=[]
        self.button_add=[]
        self.ping_func = ping_func.go()
        #while self.ping_func.flag_ping==True:
        #    QTest.qWait(1000)
        with open('ip.json', 'r', encoding='utf-8') as f:
            ip = json.load(f)
        for i in ip:
            ip[i] = dict(sorted(ip[i].items(), key=lambda x: x[1]))
        for i in ip:
            self.tab.append(QWidget())
            self.tabs.addTab(self.tab[-1],i)
            self.vertical.append(QVBoxLayout(self))
            self.tab_ip.append([])
            self.tab_names.append([])
            self.labels_status.append([])
            self.button_add.append(QPushButton())
            for j in ip[i]:
                self.tab_ip[-1].append(QLineEdit())
                self.tab_names[-1].append(QLineEdit())
                lab=QLabel()
                lab.setText("Status")
                self.labels_status[-1].append(lab)
                self.tab_ip[-1][-1].setText(j)
                self.tab_ip[-1][-1].setEnabled(False)
                self.tab_names[-1][-1].setText(ip[i][j])
                self.tab_names[-1][-1].setEnabled(False)

                if self.tab_ip[-1][-1].text() in self.ping_func:
                    #self.tab_names[-1][-1].setStyleSheet("background-color:green;")
                    #self.tab_ip[-1][-1].setStyleSheet("background-color:green;")
                    self.labels_status[-1][-1].setText("Online")
                    self.labels_status[-1][-1].setStyleSheet("background-color:green;")
                else:
                    #self.tab_names[-1][-1].setStyleSheet("background-color:red;")
                    #self.tab_ip[-1][-1].setStyleSheet("background-color:red;")
                    self.labels_status[-1][-1].setText("Offline")
                    self.labels_status[-1][-1].setStyleSheet("background-color:red;")
                horizontal=QHBoxLayout(self)
                horizontal.addWidget(self.tab_ip[-1][-1])
                horizontal.addWidget(self.tab_names[-1][-1])
                horizontal.addWidget(self.labels_status[-1][-1])
                self.vertical[-1].addLayout(horizontal)
            self.button_add[-1].setText("Add")
            self.button_add[-1].setEnabled(False)
            self.vertical[-1].addWidget(self.button_add[-1])
            self.button_add[-1].clicked.connect(self.event_button_add)
            self.vertical[-1].addStretch(0)
            self.tab[-1].setLayout(self.vertical[-1])
        self.check.setEnabled(True)
        self.spin.setEnabled(True)
        # self.tab_names[-1][-1].setStyleSheet("background-color:red;")
        # print(self.tab_names[-1][-1].text())
        #self.tab_names[0][-1].setText("sdrfg")
        #print(self.ping_func.mass)
        #print(self.check.isChecked())
        #print(self.spin.value())

    def update_ping(self):
        #print("Timer stop")
        self.check.setEnabled(False)
        self.spin.setEnabled(False)
        self.timer.stop()
        self.ping_func = ping_func.go()
        #while self.ping_func.flag_ping==True:
        #    QTest.qWait(1000)

        for i in range(len(self.tab_ip)):
            for j in range(len(self.tab_ip[i])):
                if self.tab_ip[i][j].text() in self.ping_func:
                    #self.tab_names[i][j].setStyleSheet("background-color:green;")
                    #self.tab_ip[i][j].setStyleSheet("background-color:green;")
                    self.labels_status[i][j].setText("Online")
                    self.labels_status[i][j].setStyleSheet("background-color:green;")
                else:
                    #self.tab_names[i][j].setStyleSheet("background-color:red;")
                    #self.tab_ip[i][j].setStyleSheet("background-color:red;")
                    self.labels_status[i][j].setText("Offline")
                    self.labels_status[i][j].setStyleSheet("background-color:red;")
        self.check.setEnabled(True)
        self.spin.setEnabled(True)
        self.change()
        print(self.ping_func)

    def change(self):
        if self.check.isChecked():
            self.timer.start(int(self.spin.value())*1000*60)
        else:
            self.timer.stop()

    def event_button(self):
        self.timer.stop()
        if self.button.text()=="Редактировать":
            for i in range(len(self.tab_ip)):
                for j in range(len(self.tab_ip[i])):
                    self.tab_ip[i][j].setEnabled(True)
                    self.tab_names[i][j].setEnabled(True)
            for i in range(len(self.button_add)):
                self.button_add[i].setEnabled(True)
            self.button.setText("Сохранить")
        else:
            #print(self.tabs.tabText(1))
            ip={}
            for i in range(len(self.tab_ip)):
                ip[self.tabs.tabText(i)]={}
                for j in range(len(self.tab_ip[i])):
                    if self.tab_ip[i][j].text()!="" and self.tab_names[i][j].text()!="":
                        ip[self.tabs.tabText(i)][self.tab_ip[i][j].text()]=self.tab_names[i][j].text()
            #print(ip)
            with open('ip.json', 'w', encoding='utf-8') as f:
                json.dump(ip,f)
            for i in range(len(self.tab_ip)):
                for j in range(len(self.tab_ip[i])):
                    self.tab_ip[i][j].setEnabled(False)
                    self.tab_names[i][j].setEnabled(False)
            for i in range(len(self.button_add)):
                self.button_add[i].setEnabled(False)
            self.button.setText("Редактировать")
            self.change()

    def event_button_add(self):
        self.tab_ip[self.tabs.currentIndex()].append(QLineEdit())
        self.tab_names[self.tabs.currentIndex()].append(QLineEdit())
        lab = QLabel()
        lab.setText("Status")
        self.labels_status[self.tabs.currentIndex()].append(lab)
        horizontal=QHBoxLayout(self)
        horizontal.addWidget(self.tab_ip[self.tabs.currentIndex()][-1])
        horizontal.addWidget(self.tab_names[self.tabs.currentIndex()][-1])
        horizontal.addWidget(self.labels_status[self.tabs.currentIndex()][-1])
        self.vertical[self.tabs.currentIndex()].insertLayout(self.vertical[self.tabs.currentIndex()].count()-2,horizontal)
        #print(self.tabs.currentIndex())
        #print(self.vertical[0].count())

    def eventSearch(self):
        find=""
        for i in range(len(self.tab_ip)):
            for j in range(len(self.tab_ip[i])):
                if self.searchText.text() in self.tab_ip[i][j].text() or self.searchText.text() in self.tab_names[i][j].text():
                    find+=f"{self.tab_ip[i][j].text()} {self.tab_names[i][j].text()}\n"
        msgBox = QMessageBox()
        msgBox.setText(find)
        #msgBox.setDetailedText("Place free up disk space")
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("Результаты поиска")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
