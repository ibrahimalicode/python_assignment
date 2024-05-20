from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog
from utils.generalFunctions import *
from pages.sidebar import SideBarScreen
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

        conn = sqlite3.connect("db/db.db")
        cursor = conn.cursor()

        try:
            # the code
            sql = "SELECT * FROM users WHERE email = ?"
            cursor.execute(sql, (email,))
            user = cursor.fetchone()

            if not user:
                self.errorLabel.setText("User not found !")
            elif bcrypt.checkpw(password.encode("utf-8"), user[3]):
                #print(f'user: {str(user)}')
                self.errorLabel.setText("")
                store_id(user[0])
                #retrieve_id()
                self.goToSideBar()
            else:
                self.errorLabel.setText("Invalid Password !")
            
        except sqlite3.Error as e:
            #the code
            print(f"Error: {str(e)}")


