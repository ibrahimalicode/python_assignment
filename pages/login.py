from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog
from utils.generalFunctions import *
from pages.sidebar import SideBarScreen
from api.fetch import login_user
import sqlite3
import bcrypt


loginUI = "components/login.ui"

class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        fix_ui_file(loginUI)
        loadUi(loginUI, self)
        self.loginBtn.clicked.connect(self.logUser)
        self.toCreateAccBtn.clicked.connect(self.goToRegister)
        self.ibrahimAliBtn.clicked.connect(lambda: openLink("https://www.ibrahimali.net"))

    def goToRegister(self):
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)
    
    def goToSideBar(self):
        sideBar = SideBarScreen()
        self.widget.addWidget(sideBar)
        self.widget.setCurrentIndex(self.widget.currentIndex()+2)
    
    def logUser(self):
        email = self.emailField.text()
        password = self.passwordField.text()

        if checkAndSetBorder(self.emailField, email):
            self.errorLabel.setText("Please fill the email")
            return
        if checkAndSetBorder(self.passwordField, password):
            self.errorLabel.setText("Please fill the password")
            return
        
        self.errorLabel.setText("")
        #print(f"Email: {email}\nPassword: {password}")

        res = login_user(email, password)

        if res["statusCode"] == 404: self.errorLabel.setText("User not found !")
        if res["statusCode"] == 301: self.errorLabel.setText("Invalid Password !")
        if res["statusCode"] == 501: self.errorLabel.setText("Bir hata oluştu. Tekrar deneyin !")
        if res["statusCode"] == 200: self.errorLabel.setText(""), self.goToSideBar()
        print(res)


