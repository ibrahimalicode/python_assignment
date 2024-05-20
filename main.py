import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from pages.register import RegisterScreen
from pages.login import LoginScreen
from pages.sidebar import SideBarScreen
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()

# Create an instance of the screens
login = SideBarScreen() #LoginScreen()
register = RegisterScreen()

widget.addWidget(login)
widget.addWidget(register)

widget.setMinimumWidth(500)
#widget.setMinimumHeight(808)
widget.show()

# Making widgets accessible globally
RegisterScreen.widget = widget
LoginScreen.widget = widget
SideBarScreen.widget = widget



try:
    sys.exit(app.exec())
except:
    print("Exiting")


#pyside6-rcc5  components/resources.py -o resource_rc.qrc
