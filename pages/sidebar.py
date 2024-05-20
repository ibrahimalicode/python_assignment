from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QListView
import sqlite3
from PyQt5.QtGui import QStandardItemModel, QStandardItem

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
        self.insert_item_data(get_questions("all"), 'quest')
    
    def goToLogin(self):
        self.widget.setCurrentIndex(self.widget.currentIndex()-1)

    def insert_item_data(self, data, page):
        list_view = None
        if page == 'quest':
            list_view = self.questionsPage.findChild(QListView)
        elif page == 'ans':  
            list_view = self.answersPage.findChild(QListView)
        
        if list_view:
            model = QStandardItemModel()
            list_view.setModel(model)

            try:
                if data:
                    model.appendRow(QStandardItem('Results'))
                    for i, row in enumerate(data):
                        item = QStandardItem(row[0])
                        model.appendRow(item)
                
                else: model.appendRow(QStandardItem('No Results'))
            except sqlite3.Error as e:
                print(f'Error: {str(e)}')
                model.appendRow(QStandardItem('No Results'))
            finally:
                return
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
        for data in get_questions("with_id"):
            print(str(data))
        self.stackedWidget.setCurrentIndex(3) 
        self.searchFrame.hide()

    def on_editQBtn2_toggled(self):
        #EDIT Question Page
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

