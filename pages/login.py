from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog
from utils.generalFunctions import *
from pages.sidebar import SideBarScreen
from api.fetch import login_user


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
        total_widgets = self.widget.count()
        index = total_widgets - 1
        self.widget.setCurrentIndex(self.widget.currentIndex() + index)
    
    def logUser(self):
        email = self.emailField.text()
        password = self.passwordField.text()

        if checkAndSetBorder(self.emailField, email):
            self.errorLabel.setText("Lütfen E-Posta alanını doldurun 😡!")
            return
        if checkAndSetBorder(self.passwordField, password):
            self.errorLabel.setText("Lütfen şifre alanını doldurun 😤!")
            return
        
        self.errorLabel.setText("")
        #print(f"Email: {email}\nPassword: {password}")

        res = login_user(email, password)

        if res["statusCode"] == 404: self.errorLabel.setText("Kullanıcı bulunumadı 🤷‍♂️!")
        if res["statusCode"] == 301: self.errorLabel.setText("Yanlış Şifre 🙅‍♂️!")
        if res["statusCode"] == 501: self.errorLabel.setText("Bir hata oluştu. Tekrar deneyin !")
        if res["statusCode"] == 200: self.errorLabel.setText(""), self.goToSideBar()
        print(res)


