from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
import json
import threading

user_id_path = 'json/local_storage.json'

## OPEN LINKS
def openLink(link):
    QDesktopServices.openUrl(QUrl(link))

## checkAndSetBorder
def checkAndSetBorder(field, value):
    if not value:
        new_style = field.styleSheet().replace("border-color: transparent;\n", "border-color: red;\n")
        field.setStyleSheet(new_style)
        return True  
    else:
        field.setStyleSheet(field.styleSheet().replace("border-color: red;\n", "border-color: transparent;\n"))
        return False


# Storing data
def store_id(user_id):
    data = {'userID': user_id}
    with open(user_id_path, 'w') as file:
        json.dump(data, file)
    #print(f'Stored ID: {user_id}')

# Retrieving data
def retrieve_id():
    try:
        with open(user_id_path, 'r') as file:
            data = json.load(file)
            user_id = data.get('userID', None)
    except FileNotFoundError:
        #print("File not found.")
        user_id = None
    except json.JSONDecodeError:
        #print("Invalid JSON format.")
        user_id = None
    except Exception as e:
        #print(f"An unexpected error occurred: {e}")
        user_id = None
    
    #print(f'Retrieved ID: {user_id}')
    return user_id


## DELAYED EXCUTION
def set_timeout(delay, func):
    timer = threading.Timer(delay, func)
    timer.start()


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
        'QFrame::Shadow::Plain' : 'QFrame::Plain'
    }

    with open(ui_file, 'r') as file:
        content = file.read()

    for old, new in replacements.items():
        content = content.replace(old, new)

    with open(ui_file, 'w') as file:
        file.write(content)
