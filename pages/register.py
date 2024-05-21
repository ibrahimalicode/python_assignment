from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog
from utils.generalFunctions import *
#from pages.login import LoginScreen
import sqlite3
from PyQt5.QtWidgets import QMessageBox
import bcrypt

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

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        
        if checkAndSetBorder(self.nameField, name) or \
            checkAndSetBorder(self.emailField, email) or \
            checkAndSetBorder(self.passwordField, password):
            return
        
        #print(f"Name: {name}\nEmail: {email}\nPassword: {password}")
        conn = sqlite3.connect("db/db.DB")
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                self.errorLabel_2.setText("The user exists with this email.")
                return
            
            # Insert the data into the database
            sql = "INSERT INTO users (name, email, password) VALUES (?, ?, ?)"
            cursor.execute(sql, (name, email, hashed_password))
            conn.commit()

            self.errorLabel_2.setText("")
            shop_popup("Success", "User created successfully!", "info", None)
            self.goToLogin()
            
        except sqlite3.Error as e:
            shop_popup("Error", f"Error inserting user into database: {str(e)}", "error", None)
            print( "Error", f"Error inserting user into database: {str(e)}")
            
        finally:
            conn.close()


    def goToLogin(self):
        #login = LoginScreen()
        #self.widget.addWidget(login)
        self.widget.setCurrentIndex(self.widget.currentIndex()-1)
 