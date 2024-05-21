from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog
from utils.generalFunctions import *
#from pages.login import LoginScreen
from api.fetch import *
from PyQt5.QtWidgets import QMessageBox


registerUI = "components/register.ui"

class RegisterScreen(QDialog):
    def __init__(self):
        super(RegisterScreen, self).__init__()
        fix_ui_file(registerUI)
        loadUi(registerUI, self)
        
        self.createAccBtn.clicked.connect(self.createUser)
        self.toLoginBtn.clicked.connect(self.goToLogin)
        self.ibrahimAliBtn.clicked.connect(lambda: openLink("https://www.ibrahimali.net"))
    

    
    def createUser(self):
        name = self.nameField.text()
        email = self.emailField.text()
        password = self.passwordField.text()
        
        if checkAndSetBorder(self.nameField, name) or \
            checkAndSetBorder(self.emailField, email) or \
            checkAndSetBorder(self.passwordField, password):
            return
        
        #print(f"Name: {name}\nEmail: {email}\nPassword: {password}")
        res = register_user(name, email, password)
        if res["statusCode"] == 300:
            self.errorLabel_2.setText("The user exists with this email.")
        elif res["statusCode"] == 200:
            self.errorLabel_2.setText("")
            shop_popup("Success", "User created successfully!", "info", None)
            self.goToLogin()
        elif res["statusCode"] == 501:
            shop_popup("Error", "Enternal error", "error", None)


    def goToLogin(self):
        #login = LoginScreen()
        #self.widget.addWidget(login)
        self.widget.setCurrentIndex(self.widget.currentIndex()-1)
 