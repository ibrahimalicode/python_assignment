from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
import json
import threading
from PyQt5.QtWidgets import QMessageBox
import os

user_id_path = 'json/local_storage.json'

## OPEN LINKS
def openLink(link):
    QDesktopServices.openUrl(QUrl(link))

## checkAndSetBorder
def checkAndSetBorder(field, value):
    if not value:
        current_style = field.styleSheet()
        new_style = f"{current_style} border-color: red;\n"
        field.setStyleSheet(new_style)
        return True  
    else:
        field.setStyleSheet(field.styleSheet().replace("border-color: red;\n", ""))
        return False


# Storing Id
def store_data(dataIn):
    data = {
        "userID": dataIn[0],
        "name": dataIn[1],
        "email": dataIn[2]
        }

    with open(user_id_path, 'w') as file:
        json.dump(data, file)
    #print(f'Stored ID: {user_id}')

# Retrieving ID
def retrieve_data():
    try:
        with open(user_id_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        #print("File not found.")
        data = None
    except json.JSONDecodeError:
        #print("Invalid JSON format.")
        data = None
    except Exception as e:
        #print(f"An unexpected error occurred: {e}")
        data = None
    
    #print(f'Retrieved ID: {user_id}')
    return data

# Removing ID
def remove_data():
    try:
        if os.path.exists(user_id_path):
            os.remove(user_id_path)
            print(f"User ID file '{user_id_path}' has been removed.")
        else:
            print(f"User ID file '{user_id_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred while trying to remove the user ID file: {e}")


## DELAYED EXCUTION
def set_timeout(delay, func):
    timer = threading.Timer(delay, func)
    timer.start()


##POP UP
button_val = None
def popup_button(i):
    global button_val
    button_val = i.text()  # Get the text of the button clicked
    #print(f"btn {button_val}")
    #print(f"i = {i.text()}")

def shop_popup(text, info, type, btn):
    global button_val
    msg = QMessageBox()
    #msg.setWindowTitle("Success") ## Not needed

    if text: 
        msg.setText(text)
    if info: 
        msg.setInformativeText(info)

    if type == "warning":
        msg.setIcon(QMessageBox.Warning)
    elif type == "question":
        msg.setIcon(QMessageBox.Question)
    elif type == "error":
        msg.setIcon(QMessageBox.Critical)
    elif type == "info":
        msg.setIcon(QMessageBox.Information)

    # Add specific buttons and connect their clicked signals
    if btn:
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    else:
        msg.setStandardButtons(QMessageBox.Ok)
    
    msg.buttonClicked.connect(popup_button)

    x = msg.exec_()
    
    #print(f"btn {button_val}")

    return button_val


## FIX UI FILES
def fix_ui_file(ui_file):
    replacements = {
        'Qt::AlignmentFlag::AlignCenter': 'Qt::AlignCenter',
        'Qt::LayoutDirection::LeftToRight': 'Qt::LeftToRight',
        'QFrame::Shape::StyledPanel': 'QFrame::StyledPanel',
        'QFrame::Shadow::Raised': 'QFrame::Raised',
        'Qt::AlignmentFlag::AlignHCenter': 'Qt::AlignHCenter',
        'Qt::AlignmentFlag::AlignVCenter': 'Qt::AlignVCenter',
        'Qt::AlignmentFlag::AlignBottom': 'Qt::AlignBottom',
        'QLayout::SizeConstraint::SetDefaultConstraint': 'QLayout::SetDefaultConstraint',
        'QLineEdit::EchoMode::Password' : 'QLineEdit::Password',
        'QLineEdit::EchoMode::Email' : 'QLineEdit::Email',
        'Qt::AlignmentFlag::AlignRight' : 'Qt::AlignRight',
        'Qt::AlignmentFlag::AlignLeft' : 'Qt::AlignLeft',
        'Qt::Orientation::Vertical' : 'Qt::Vertical',
        'Qt::Orientation::Horizontal' : 'Qt::Horizontal',
        'QListView::ResizeMode::Adjust' : 'QListView::Adjust',
        'QListView::ResizeMode::Fixed' : 'QListView::Fixed',
        'Qt::AlignmentFlag::AlignLeading' : 'Qt::AlignLeading',
        'Qt::ScrollBarPolicy::ScrollBarAlwaysOff' : 'Qt::ScrollBarAlwaysOff',
        'QAbstractItemView::SelectionMode::NoSelection' : 'QAbstractItemView::NoSelection',
        'QAbstractItemView::SelectionMode::SingleSelection' : 'QAbstractItemView::SingleSelection',
        'Qt::AlignmentFlag::AlignTop' : 'Qt::AlignTop',
        'QFrame::Shadow::Plain' : 'QFrame::Plain',
        'QAbstractItemView::SelectionBehavior::SelectRows' : 'QAbstractItemView::SelectRows',
        'QAbstractItemView::SelectionBehavior::SelectItems' : 'QAbstractItemView::SelectItems',
    }

    with open(ui_file, 'r') as file:
        content = file.read()

    for old, new in replacements.items():
        content = content.replace(old, new)

    with open(ui_file, 'w') as file:
        file.write(content)
