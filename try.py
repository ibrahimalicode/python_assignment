from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QDialog, QListView
import sqlite3

from PyQt5.QtCore import Qt

def insert_item_data(self, data, page):
    list_view = None
    if page == 'quest':
        list_view = self.questionsPage.findChild(QListView)
    elif page == 'ans':  
        list_view = self.answersPage.findChild(QListView)
    elif page == "edit_question":
        list_view = self.editQPage.findChild(QListView)
    
    if list_view:
        model = QStandardItemModel()
        list_view.setModel(model)

        try:
            if data:
                model.appendRow(QStandardItem('Results'))
                for i, row in enumerate(data):
                    item = QStandardItem(row[0])
                    item.setData(row[1], Qt.UserRole)  # Storing question ID as custom data
                    model.appendRow(item)
            
            else: 
                model.appendRow(QStandardItem('No Results'))
        except sqlite3.Error as e:
            print(f'Error: {str(e)}')
            model.appendRow(QStandardItem('No Results'))
    else:
        print(f'No list found to insert the data')
