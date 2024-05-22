import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from pages.register import RegisterScreen
from pages.login import LoginScreen
from pages.sidebar import SideBarScreen
from pages.confirm import ConfirmScreen

app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()

# Create an instance of the screens
#login = SideBarScreen() ## i don't have to login everytime to see the sidebar when working.
login = LoginScreen() 
register = RegisterScreen()

widget.addWidget(login)
widget.addWidget(register)

#widget.setFixedWidth(500)  ## WE can do these in the designer. so no need to set it here.
#widget.setMinimumWidth(500)
#widget.setMinimumHeight(808)
widget.show()

## SET THE PAGE TO CENTER OF THE SCREEN (took it from chatGPT)
screen_geometry = app.desktop().availableGeometry() # get the total screen size of the computer
x = (screen_geometry.width() - widget.width()) // 2 
y = (screen_geometry.height() - widget.height()) // 2
widget.move(x, y)


# Making widgets accessible globally
LoginScreen.widget = widget
RegisterScreen.widget = widget
SideBarScreen.widget = widget
ConfirmScreen.widget = widget



try:
    sys.exit(app.exec())
except:
    print("Exiting...")


