import resources_rc
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from api.loading_func import GPTResponseThread
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QMovie
from PyQt5.QtWidgets import QDialog, QListView, QApplication, QLabel


## FUNCTIONS
from utils.generalFunctions import *
from api.fetch import *


sideBarUI = "components/sidebar.ui"

""" class GPTResponseThread(QThread):
    response_received = pyqtSignal(str)

    def __init__(self, prompt):
        super().__init__()
        self.prompt = prompt

    def run(self):
        response = get_gpt_response(self.prompt)
        self.response_received.emit(response) """

class SidebarScreen(QDialog):
    def __init__(self):
        super(SidebarScreen, self).__init__()
        fix_ui_file(sideBarUI)
        loadUi(sideBarUI, self)

        self.icon_only_widget.hide()
        self.stackedWidget.setCurrentIndex(0)
        self.questionsBtn2.setChecked(True)
        self.logo.clicked.connect(lambda: openLink("https://www.ibrahimali.net"))
        self.logo_2.clicked.connect(lambda: openLink("https://www.ibrahimali.net"))

        self.searchBtn.clicked.connect(self.handle_search)
        self.searchBar.returnPressed.connect(self.handle_search)

        self.addQuestionBtn.clicked.connect(lambda: self.addElement("Question"))
        self.addAnswerBtn.clicked.connect(lambda: self.addElement("Answer"))

        self.editQBtn_2.clicked.connect(lambda: self.edit_element("Question"))
        self.saveQBtn_2.clicked.connect(lambda: self.save_element("Question"))
        self.deleteQBtn_2.clicked.connect(lambda: self.delete_element("Question"))

        self.editABtn_2.clicked.connect(lambda: self.edit_element("Answer"))
        self.saveABtn_2.clicked.connect(lambda: self.save_element("Answer"))
        self.deleteABtn_2.clicked.connect(lambda: self.delete_element("Answer"))

        self.logoutBtn.clicked.connect(self.logout)
        self.logoutBtn2.clicked.connect(self.logout)

        self.savePassword.clicked.connect(self.updatePassword)
        self.savePersonalInfoBtn.clicked.connect(self.updateName)

        self.insert_item_data(get_item("all", "Question"), 'quest')


        # Loading indicator setup
        self.loadingLabel.move(400,300)
        self.loadingLabel = QLabel(self)
        self.loadingLabel.setMovie(QMovie("components/loading.gif"))
        self.loadingLabel.setVisible(False)
    
    # Declare Global Variables
    edit_element_text = None
    edit_element_id = None
    is_selected_element_row = False
    gpt_conversation = []

    def show_loading(self):
        self.loadingLabel.setVisible(True)
        self.loadingLabel.movie().start()

    def hide_loading(self):
        self.loadingLabel.setVisible(False)
        self.loadingLabel.movie().stop()

    def goToLogin(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() - 1)

    def insert_item_data(self, data, page):
        list_view = None
        if page == 'quest':
            list_view = self.questionsPage.findChild(QListView)
        elif page == 'ans':  
            list_view = self.answersPage.findChild(QListView)
        elif page == "edit_question":
            list_view = self.editQPage.findChild(QListView)
        elif page == "edit_answer":
            list_view = self.editAPage.findChild(QListView)
        
        if list_view:
            model = QStandardItemModel()
            list_view.setModel(model)

            try:
                if data:
                    model.appendRow(QStandardItem('Results'))
                    for i, row in enumerate(data):
                        item = QStandardItem(row[0])
                        if page == "edit_question" or page == "edit_answer":
                            item.setData(row[2], Qt.UserRole)  # Storing question/answer ID as custom data
                        model.appendRow(item)
                else:
                    model.appendRow(QStandardItem('No Results'))
            except sqlite3.Error as e:
                print(f'Error: {str(e)}')
                model.appendRow(QStandardItem('No Results'))
        else:
            print(f'No list found to insert the data')

    def handle_search(self):
        prompt = self.searchBar.text().strip()
        if not prompt:
            if  self.stackedWidget.currentIndex() == 0:
                self.insert_item_data(get_item("all", "Question"), 'quest')
            elif  self.stackedWidget.currentIndex() == 1:
                self.insert_item_data(get_item("all", "Answer"), 'ans')
            return

        self.gpt_conversation.append([f'soru:\n {prompt}'])
        add_element(prompt, "Question")
        
        # Show loading indicator
        self.show_loading()

        # Start the GPT response thread
        self.gpt_response_thread = GPTResponseThread(prompt)
        self.gpt_response_thread.response_received.connect(self.handle_gpt_response)
        self.gpt_response_thread.start()

    def handle_gpt_response(self, response):
        self.hide_loading()
        self.searchBar.setText("")
        self.gpt_conversation.append([f'cevap:\n {response}'])
        add_element(response, "Answer")
        
        if self.stackedWidget.currentIndex() == 0:
            self.insert_item_data(self.gpt_conversation, "quest")
        elif self.stackedWidget.currentIndex() == 1:
            self.insert_item_data(self.gpt_conversation, "ans")

        print(str(self.gpt_conversation))

    ## functions for changing menu page
    # questions page
    def on_questionsBtn_toggled(self):
        self.stackedWidget.setCurrentIndex(0)
        if not self.gpt_conversation:
            self.insert_item_data(get_item("all", "Question"), 'quest')
        self.searchFrame.show()
    
    # questions page
    def on_questionsBtn2_toggled(self):
        self.stackedWidget.setCurrentIndex(0)
        if not self.gpt_conversation:
            self.insert_item_data(get_item("all", "Question"), 'quest')
        self.searchFrame.show()

    # answers page
    def on_answersBtn_toggled(self):
        self.stackedWidget.setCurrentIndex(1)
        self.insert_item_data(get_item("all", "Answer"), 'ans')
        self.searchFrame.show()

    # answers page
    def on_answersBtn2_toggled(self):
        self.stackedWidget.setCurrentIndex(1)
        self.insert_item_data(get_item("all", "Answer"), 'ans')
        self.searchFrame.show()

    # ADD Question Page
    def on_addQBtn_toggled(self):
        self.stackedWidget.setCurrentIndex(2)
        self.searchFrame.hide()

    # ADD Question Page
    def on_addQBtn2_toggled(self):
        self.stackedWidget.setCurrentIndex(2) 
        self.searchFrame.hide()

    #EDIT Question Page
    def on_editQBtn_toggled(self):
        self.insert_item_data(get_item("with_id", "Question"), 'quest')
        self.stackedWidget.setCurrentIndex(3) 
        self.searchFrame.hide()

    #EDIT Question Page
    def on_editQBtn2_toggled(self):
        self.insert_item_data(get_item("with_id", "Question"), 'edit_question')
        self.stackedWidget.setCurrentIndex(3)
        self.searchFrame.hide()

    #ADD Answer Page
    def on_addABtn_toggled(self):
        self.stackedWidget.setCurrentIndex(4) 
        self.searchFrame.hide()

    #ADD Answer Page
    def on_addABtn2_toggled(self):
        self.stackedWidget.setCurrentIndex(4)
        self.searchFrame.hide()

    #EDIT Answer Page
    def on_editABtn_toggled(self):
        self.insert_item_data(get_item("with_id", "Answer"), 'edit_answer')
        self.stackedWidget.setCurrentIndex(5) 
        self.searchFrame.hide()

    #EDIT Answer Page
    def on_editABtn2_toggled(self):
        self.insert_item_data(get_item("with_id", "Answer"), 'edit_answer')
        self.stackedWidget.setCurrentIndex(5)
        self.searchFrame.hide()

    ## PROFILE page
    def on_profileBtn_toggled(self):
        self.stackedWidget.setCurrentIndex(6)
        self.searchFrame.hide()
        data = retrieve_data()
        self.fullName.setText(data["name"])
        self.email.setText(data["email"])
        self.oldPassword.setText("")
        self.newPassword.setText("")
        self.confirmPassword.setText("")

    ## PROFILE page
    def on_profileBtn2_toggled(self):
        self.stackedWidget.setCurrentIndex(6) 
        self.searchFrame.hide()
        data = retrieve_data()
        self.fullName.setText(data["name"])
        self.email.setText(data["email"])
        self.oldPassword.setText("")
        self.newPassword.setText("")
        self.confirmPassword.setText("")


    ## SET STYLES
    def setStyles(self, state, element): 

        e = None
        if element == "Answer":
            e = self.addNewA
        elif element == "Question":
            e = self.addNewQ
            
        
        if state == 'true':
            e.setStyleSheet("color: green;")
            e.setText(f'{element} added successfully!')
        elif state == 'false':
            e.setStyleSheet("color: red;")
            e.setText(f'Please enter a {element} !')
        else:
            e.setStyleSheet("")
            e.setText(f'Add new {element}')


    ## ADD ELEMENT(QUESTION/ANSWER)
    def addElement(self, element):
        text = None
        input = None

        if element == "Question":
            text = self.addQInput.toPlainText().strip()
            input = self.addQInput
        if element == "Answer":
            text = self.addAInput.toPlainText().strip()
            input = self.addAInput
        

        if not text:
            self.setStyles("false", element)
            set_timeout(2, lambda: self.setStyles("", element))
            return
        else:
            res = add_element(text, element)
            if res["statusCode"] == 200:
                #print(text)
                self.setStyles("true", element)
                input.clear()
                set_timeout(3, lambda: self.setStyles("", element)) 
            elif res["statusCode"] == 401:
                print("Unauthorized")
                self.goToLogin()
            else:
                print(f"Error adding question: {res['statusCode']}")


    ## EDIT ELEMENT(QUESTION/ANSWER)
    def edit_element(self, element):
        list_view = None
        input = None

        if element == "Question":
            list_view = self.editQPage.findChild(QListView, 'editQList')
            input = self.editQInput
        if element == "Answer":
            list_view = self.editAPage.findChild(QListView, 'editAList')
            input = self.editAInput
            
        if list_view:
            selected_index = list_view.currentIndex()
            selected_row = list_view.currentIndex().row()
            if selected_row != -1:
                item = list_view.model().item(selected_row).text().strip()
                self.edit_element_id = list_view.model().data(selected_index, Qt.UserRole)  # Retrieve the ID
                self.edit_element_text = item
                self.is_selected_element_row = True
                input.setText(item)
            else:
                shop_popup("Information", "Please select a row", "info", None)
                self.is_selected_element_row = False
        else:
            print("List view not found")


    ## SAVE ELEMENT(QUESTION/ANSWER)
    def save_element(self, element):
        list_view = None
        entity = None
        input = None

        if element == "Question":
            list_view = self.editQPage.findChild(QListView, 'editQList')
            entity = self.editQInput.toPlainText().strip()
            input = self.editQInput
        if element == "Answer":
            list_view = self.editAPage.findChild(QListView, 'editAList')
            entity = self.editAInput.toPlainText().strip()
            input = self.editAInput

        selected_row = list_view.currentIndex().row()
        

        if selected_row == -1: 
            #print(f'row: {self.is_selected_element_row}, text: {self.edit_element_text}, id: {self.edit_element_id}')
            shop_popup("Information", "Please select a row", "info", None)
            return
        
        if entity ==  self.edit_element_text:
            shop_popup("Information", "No change has made, Please make sure you have made a change!", "info", None)
        elif entity: 
            res = update_element(entity, self.edit_element_id, element)
            if res["statusCode"] == 200:
                    # empty the edit input after editing
                    input.setText("")
                    # Update the item text in the list view
                    model = list_view.model()
                    item = model.item(selected_row)
                    item.setText(entity)                 
                    shop_popup("Information", f"The {element} updated successfully", "info", None)
            elif res["statusCode"] == 401:
                shop_popup("Warning", "Un authorized", "warning", None)
        else:
            shop_popup("Information", "Please edit the element to save it.", "info", None)


    ## DELETE ELEMENT(QUESTION/ANSWER)
    def delete_element(self, element):
        list_view = None
        input = None

        if element == "Question":
            list_view = self.editQPage.findChild(QListView, 'editQList')
            input = self.editQInput
        if element == "Answer":
            list_view = self.editAPage.findChild(QListView, 'editAList')
            input = self.editAInput

        selected_row = list_view.currentIndex().row()
        if selected_row == -1:  
            #print(f'row: {self.is_selected_element_row}, text: {self.edit_element_text}, id: {self.edit_element_id}')
            shop_popup("Information", "Please select a row", "info", None)
            return
        else: 
            if shop_popup("Warning", "Are you sure you want to delete the selected item ?", "warning", True) == "OK":
                #print(f'id : {self.edit_element_id}')
                res = destroy_element(self.edit_element_id, element)
                if res["statusCode"] == 200:
                    # Delete the row from the model
                    model = list_view.model()
                    model.removeRow(selected_row)
                    # empty the edit input after deletion
                    input.setText("")
                    # show  a message to user
                    shop_popup("Information", f"The {element} deleted successfully", "info", None)
                elif res["statusCode"] == 401:
                    shop_popup("Warning", "Un authorized", "warning", None)

    
    ## LOGOUT USER AND CLOSE THE APP
    def logout(self):
        print("Logging out...")
        # Close the application
        remove_data()
        QApplication.quit()

    ##UPDATE PASSWORD
    def updatePassword(self):
        oldPassword = self.oldPassword.text()
        newPassword = self.newPassword.text()
        confirmPassword = self.confirmPassword.text()

             
        if checkAndSetBorder(self.oldPassword, oldPassword) or \
            checkAndSetBorder(self.newPassword, newPassword) or \
            checkAndSetBorder(self.confirmPassword, confirmPassword):
            return

        if newPassword != confirmPassword:
            shop_popup("Bilgilendirme", "Yeni şifreleriniz aynı değildir. Lütfen kontrol edin!", "warning", None)
            return
        elif oldPassword == confirmPassword:
            shop_popup("Bilgilendirme", "Hiç bir değişiklik yapmadınız. Lütfen kontrol edin!", "warning", None)
            return
        else: 
            res = update_password(newPassword, oldPassword)
            if res["statusCode"] == 200: 
                shop_popup("Bilgilendirme", "Şifreniz başarıyla güncellendi!", "info", None)
                self.oldPassword.setText("")
                self.newPassword.setText("")
                self.confirmPassword.setText("")
            if res["statusCode"] == 501: shop_popup("Hata", "Bir hata oluştu. Tekrar deneyiniz!", "error", None)
            if res["statusCode"] == 401: shop_popup("Hata", "Eski şifrenizi yanlış girdiniz!", "error", None)

    ##UPDATE NAME
    def updateName(self):
        oldName = retrieve_data()["name"]
        newName = self.fullName.text()

        if checkAndSetBorder(self.fullName, newName): return
        if oldName == newName: 
            shop_popup("Bilgilendirme", "Hiç bir değişiklik yapmadınız. Lütfen kontrol edin!", "warning", None)
            return
        res = update_name(newName)
        if res["statusCode"] == 200:
            shop_popup("Bilgilendirme", "Adınız başarıyla güncellendi!", "info", None)
        if res["statusCode"] == 501: shop_popup("Hata", "Bir hata oluştu. Tekrar deneyiniz!", "error", None)