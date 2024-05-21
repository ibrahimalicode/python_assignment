from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QListView
import sqlite3
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt

## FUNCTIONS
from utils.generalFunctions import *
from api.fetch import *

sideBarUI = "components/sidebar.ui"


class SideBarScreen(QDialog):
    def __init__(self):
        super(SideBarScreen, self).__init__()
        fix_ui_file(sideBarUI)
        loadUi(sideBarUI, self)

        self.icon_only_widget.hide()
        self.stackedWidget.setCurrentIndex(0)
        self.questionsBtn2.setChecked(True)
        self.addQuestionBtn.clicked.connect(self.addQuestion)
        self.addAnswerBtn.clicked.connect(self.addAnswer)
        self.logo.clicked.connect(lambda: openLink("https://www.ibrahimali.net"))
        self.logo_2.clicked.connect(lambda: openLink("https://www.ibrahimali.net"))
        self.editQBtn_2.clicked.connect(self.edit_question)
        self.saveQBtn_2.clicked.connect(self.save_question)
        self.deleteQBtn_2.clicked.connect(self.delete_question)
        self.insert_item_data(get_questions("all"), 'quest')
    
    def goToLogin(self):
        self.widget.setCurrentIndex(self.widget.currentIndex()-1)

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
                        item.setData(row[2], Qt.UserRole)  # Storing question/answer ID as custom data
                        model.appendRow(item)
                
                else: model.appendRow(QStandardItem('No Results'))
            except sqlite3.Error as e:
                print(f'Error: {str(e)}')
                model.appendRow(QStandardItem('No Results'))
        else:
            print(f'No list fount to insert the data')


    ## Function for searching
    def on_searchBtn_clicked(self):
        search_text = self.searchBar.text().strip()
        
        if search_text:
            if  self.stackedWidget.currentIndex() == 0:
                self.insert_item_data(search_questions(search_text), 'quest')
            elif  self.stackedWidget.currentIndex() == 1:
                self.insert_item_data(search_answers(search_text), 'ans')
        else:
            if  self.stackedWidget.currentIndex() == 0:
                self.insert_item_data(get_questions("all"), 'quest')
            elif  self.stackedWidget.currentIndex() == 1:
                self.insert_item_data(get_answers("all"), 'ans')


    ## functions for changing menu page
    def on_questionsBtn_toggled(self):
        # questions page
        self.stackedWidget.setCurrentIndex(0)
        self.insert_item_data(get_questions("all"), 'quest')
        self.searchFrame.show()
    
    def on_questionsBtn2_toggled(self):
        # questions page
        self.stackedWidget.setCurrentIndex(0)
        self.insert_item_data(get_questions("all"), 'quest')
        self.searchFrame.show()

    def on_answersBtn_toggled(self):
        # answers page
        self.stackedWidget.setCurrentIndex(1)
        self.insert_item_data(get_answers("all"), 'ans')
        self.searchFrame.show()

    def on_answersBtn2_toggled(self):
        # answers page
        self.stackedWidget.setCurrentIndex(1)
        self.insert_item_data(get_answers("all"), 'ans')
        self.searchFrame.show()

    def on_addQBtn_toggled(self):
        # ADD Question Page
        self.stackedWidget.setCurrentIndex(2)
        self.searchFrame.hide()

    def on_addQBtn2_toggled(self):
        # ADD Question Page
        self.stackedWidget.setCurrentIndex(2) 
        self.searchFrame.hide()

    def on_editQBtn_toggled(self):
        #EDIT Question Page
        self.insert_item_data(get_questions("with_id"), 'quest')
        self.stackedWidget.setCurrentIndex(3) 
        self.searchFrame.hide()

    def on_editQBtn2_toggled(self):
        #EDIT Question Page
        self.insert_item_data(get_questions("with_id"), 'edit_question')
        self.stackedWidget.setCurrentIndex(3)
        self.searchFrame.hide()

    def on_addABtn_toggled(self):
        #ADD Answer Page
        self.stackedWidget.setCurrentIndex(4) 
        self.searchFrame.hide()

    def on_addABtn2_toggled(self):
        #ADD Answer Page
        self.stackedWidget.setCurrentIndex(4)
        self.searchFrame.hide()

    def on_editABtn_toggled(self):
        #EDIT Answer Page
        self.stackedWidget.setCurrentIndex(5) 
        self.searchFrame.hide()

    def on_editABtn2_toggled(self):
        #EDIT Answer Page
        self.stackedWidget.setCurrentIndex(5)
        self.searchFrame.hide()

    def on_profileBtn_toggled(self):
        ## PROFILE page
        self.stackedWidget.setCurrentIndex(6)
        self.searchFrame.hide()

    def on_profileBtn2_toggled(self):
        ## PROFILE page
        self.stackedWidget.setCurrentIndex(6) 
        self.searchFrame.hide()

    ## SET STYLES
    def setStyles(self, state, element): 

        e = None
        text = None
        if element == "ans":
            e = self.addNewA
            text = "Answer"
        elif element == "ques":
            e = self.addNewQ
            text = "Question"
            
        
        if state == 'true':
            e.setStyleSheet("color: green;")
            e.setText(text + ' added successfully!')
        elif state == 'false':
            e.setStyleSheet("color: red;")
            e.setText('Please enter a ' + text + '!')
        else:
            e.setStyleSheet("")
            e.setText('Add new ' + text)


    ## HANDLE ADD QUESTION
    def addQuestion(self):
        question = self.addQInput.toPlainText().strip()

        if not question:
            self.setStyles("false", "ques")
            set_timeout(2, lambda: self.setStyles("", "ques"))
            return
        else:
            res = add_question(question)
            if res["statusCode"] == 200:
                print(question)
                self.setStyles("true", "ques")
                self.addQInput.clear()
                set_timeout(3, lambda: self.setStyles("", "ques")) 
            elif res["statusCode"] == 401:
                print("Unauthorized")
                self.goToLogin()
            else:
                print(f"Error adding question: {res['statusCode']}")


    ## HANDLE ADD ANSWER
    def addAnswer(self):
        answer = self.addAInput.toPlainText().strip()

        if not answer:
            self.setStyles("false", "ans")
            set_timeout(2, lambda: self.setStyles("", "ans"))
            return
        else:
            res = add_answer(answer)
            if res["statusCode"] == 200:
                print(answer)
                self.setStyles("true", "ans")
                self.addQInput.clear()
                set_timeout(3, lambda: self.setStyles("", "ans")) 
            elif res["statusCode"] == 401:
                print("Unauthorized")
                self.goToLogin()
            else:
                print(f"Error adding answer: {res['statusCode']}")

    ## HANDLE EDIT QUESTION
    edit_question_text = None
    edit_question_id = None
    is_selected_q_row = False
    def edit_question(self):
        list_view = self.editQPage.findChild(QListView, 'editQList')
        if list_view:
            selected_index = list_view.currentIndex()
            selected_row = list_view.currentIndex().row()
            if selected_row != -1:
                question = list_view.model().item(selected_row).text().strip()
                self.edit_question_id = list_view.model().data(selected_index, Qt.UserRole)  # Retrieve the ID
                self.edit_question_text = question
                self.is_selected_q_row = True
                self.editQInput.setText(question)
            else:
                shop_popup("Information", "Please select a row", "info", None)
                self.is_selected_q_row = False
        else:
            print("List view not found")

    def save_question(self):
        if not self.is_selected_q_row: 
            print(f'row: {self.is_selected_q_row}, text: {self.edit_question_text}, id: {self.edit_question_id}')
            shop_popup("Information", "Please select a row", "info", None)
            return
        question = self.editQInput.toPlainText().strip()
        if question ==  self.edit_question_text:
            shop_popup("Information", "No change has made, Please make sure u made a change!", "info", None)
        else: 
            res = update_question(question, self.edit_question_id)
            if res["statusCode"] == 200:
                    shop_popup("Information", "Question updated successfully", "info", None)
            elif res["statusCode"] == 401:
                shop_popup("Warning", "Un authorized", "warning", None)
    
    def delete_question(self):
        if not self.is_selected_q_row: 
            print(f'row: {self.is_selected_q_row}, text: {self.edit_question_text}, id: {self.edit_question_id}')
            shop_popup("Information", "Please select a row", "info", None)
            return
        else: 
            if shop_popup("Warning", "Are you sure you want to delete the selected item ?", "warning", True) == "OK":
                print(f'id : {self.edit_question_id}')
                res = destroy_question(self.edit_question_id)
                if res["statusCode"] == 200:
                    shop_popup("Information", "Question deleted successfully", "info", None)
                elif res["statusCode"] == 401:
                    shop_popup("Warning", "Un authorized", "warning", None)