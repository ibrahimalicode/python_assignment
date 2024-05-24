from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog
from utils.generalFunctions import *
from pages.confirm import ConfirmScreen
from api.fetch import *
from dotenv import load_dotenv
import os

load_dotenv()

link = os.getenv('WEBSITE_LINK')
registerUI = "components/register.ui"

class RegisterScreen(QDialog):
    def __init__(self):
        super(RegisterScreen, self).__init__()
        fix_ui_file(registerUI)
        loadUi(registerUI, self)
        
        self.createAccBtn.clicked.connect(self.createUser)
        self.toLoginBtn.clicked.connect(self.goToLogin)
        self.ibrahimAliBtn.clicked.connect(lambda: openLink(link))
        self.createAccBtn.setEnabled(True)  # Enable the button

    
    def createUser(self):
        name = self.nameField.text()
        email = self.emailField.text()
        password = self.passwordField.text()
        error = self.errorLabel_2
        
        if checkAndSetBorder(self.nameField, name):
            error.setText("Lütfen adı alanını doldurun 😤!")
            return
        if checkAndSetBorder(self.emailField, email):
            error.setText("Lütfen E-Posta alanını doldurun 😡!")
            return
        if checkAndSetBorder(self.passwordField, password):
            error.setText("Lütfen şifre alanını doldurun 😡!")
            return
        
        # check if the email if valid email format
        if not is_valid_email(email):
            error.setText("Lütfen oynamayın. Adam gibi geçerli bir E-Posta adresi girin! 😡")
            return
        else: error.setText("")

        #print(f"Name: {name}\nEmail: {email}\nPassword: {password}") 
        self.goToConfirm(name, email, password)
        self.nameField.setText('')
        self.emailField.setText('')
        self.passwordField.setText('')
        self.createAccBtn.setEnabled(False)  # Disable the button


    def goToConfirm(self, name, email, password):
        confirm = ConfirmScreen(name, email, password)  # Pass the data to ConfirmScreen
        self.widget.addWidget(confirm)
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)


    def goToLogin(self):
        #login = LoginScreen()
        #self.widget.addWidget(login)
        self.widget.setCurrentIndex(self.widget.currentIndex()-1)
 