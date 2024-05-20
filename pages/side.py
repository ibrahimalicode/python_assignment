from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QTableWidget, QHeaderView
from PyQt5 import QtWidgets
from utils.generalFunctions import *
import sqlite3

sideBarUI = "components/sidebar.ui"

class SideBarScreen(QDialog):
    def __init__(self):
        super(SideBarScreen, self).__init__()
        fix_ui_file(sideBarUI)
        loadUi(sideBarUI, self)

        self.icon_only_widget.hide()
        self.stackedWidget.setCurrentIndex(0)
        self.questionsBtn2.setChecked(True)
        #self.setup_table_widget()

        if self.stackedWidget.currentIndex() == 0:
            table_widget = self.questionsPage.findChild(QTableWidget, 'questionsTableWidget')
            if table_widget:
                table_widget.setHorizontalHeaderLabels(["Results"])
                table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

                conn = sqlite3.connect("db/db.db")
                cur = conn.cursor()
                sql = "SELECT * FROM questions LIMIT 50"

                try:
                    data = cur.execute(sql)
                    if data:
                        for i, row in enumerate(data):
                            table_widget.insertRow(i)
                            item = QtWidgets.QTableWidgetItem(row[0])
                            table_widget.setItem(i, 0, item)
                except sqlite3.Error as e:
                    print(f'Error: {str(e)}')
                finally:
                    conn.close()

     ## Function for searching
    def on_searchBtn_clicked(self):
        search_text = self.searchBar.text().strip()
        
        if search_text:
            if  self.stackedWidget.currentIndex() == 0:
                self.questions_label.setText(search_text)
            elif  self.stackedWidget.currentIndex() == 1:
                self.answers_label.setText(search_text)

        ## functions for changing menu page
    def on_questionsBtn_toggled(self):
        self.stackedWidget.setCurrentIndex(0)
        self.searchFrame.show()
    
    def on_questionsBtn2_toggled(self):
        self.stackedWidget.setCurrentIndex(0)
        self.searchFrame.show()

    def on_answersBtn_toggled(self):
        self.stackedWidget.setCurrentIndex(1)
        self.searchFrame.show()

    def on_answersBtn2_toggled(self):
        self.stackedWidget.setCurrentIndex(1)
        self.searchFrame.show()

    def on_profileBtn_toggled(self):
        self.stackedWidget.setCurrentIndex(2)
        self.searchFrame.hide()

    def on_profileBtn2_toggled(self):
        self.stackedWidget.setCurrentIndex(2) 
        self.searchFrame.hide()
    
        