from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog
from utils.generalFunctions import *
from api.fetch import *
from api.sendConfirmationCode import send_confirmation_code
import random

confirmUI = "components/confirm.ui"

class ConfirmScreen(QDialog):
    def __init__(self, name, email, password):
        super(ConfirmScreen, self).__init__()
        fix_ui_file(confirmUI)
        loadUi(confirmUI, self)

        # Store the passed data
        self.name = name
        self.email = email
        self.password = password
        self.confirmation_code = None  # Instance variable for the confirmation code

        # Generate the confirmation code
        self.generate_confirmation_code()

        # Connect buttons to their respective methods, pass confirmation_code to createUserConfirmed
        self.submitBtn.clicked.connect(lambda: self.createUserConfirmed(self.confirmation_code))
        self.toLoginBtn.clicked.connect(self.goToLogin)
        self.ibrahimAliBtn.clicked.connect(lambda: openLink("https://www.ibrahimali.net"))

    def generate_confirmation_code(self):
        if self.name and self.email and self.password:
            # Generate a random 4-digit confirmation code
            self.confirmation_code = ''.join(random.choices('0123456789', k=4))
            print(f"Generated confirmation_code: {self.confirmation_code}")
            #Send email
            send_confirmation_code(self.email, self.name, self.confirmation_code)

    def goToLogin(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() - 2)

    def createUserConfirmed(self, confirmation_code):
        entered_code = self.codeField.text()
        print(f"Entered code: {entered_code}")
        print(f"Passed confirmation_code: {confirmation_code}")

        if checkAndSetBorder(self.codeField, entered_code):
            self.errorLabel.setText("Lütfen doğrulama kodu giriniz 😡!")
            return
        if entered_code != confirmation_code:
            self.errorLabel.setText("Yanlış doğrulama kodu 😞!")
            return

        self.errorLabel.setText("")

        res = register_user(self.name, self.email, self.password)
        if res["statusCode"] == 300:
            self.errorLabel.setText("Bu E-Posta adres ile kulllanıcı mevcüttür 😏!")
        elif res["statusCode"] == 200:
            self.errorLabel.setText("")
            shop_popup("Success", "Başarıyla kayıt oldunuz. Eğlenemeye başlayabilirsiniz 😎", "info", None)
            self.goToLogin()
        elif res["statusCode"] == 501:
            shop_popup("Error", "Internal error", "error", None)

