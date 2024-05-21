from utils.generalFunctions import *
import sqlite3
import uuid
import bcrypt


## REGISTER USER
def register_user(name, email, password):
    conn = sqlite3.connect("db/db.DB")
    cursor = conn.cursor()
    data = {"statusCode": ""}

    id = str(uuid.uuid4())  # Generate a unique ID
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt) #Hash the password
        
    try:
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            data["statusCode"] = 300
            return data
        
        # Insert the data into the database
        sql = "INSERT INTO users (id, name, email, password) VALUES (?, ?, ?, ?)"
        cursor.execute(sql, (id, name, email, hashed_password))
        conn.commit()

        data["statusCode"] = 200
        
    except sqlite3.Error as e:
        shop_popup("Error", f"Error inserting user into database: {str(e)}", "error", None)
        print( "Error", f"Error inserting user into database: {str(e)}")
        data["statusCode"] = 501
        
    finally:
        conn.close()
    
    return data


## RELATED TO QUESTIONS
def get_item(type, element):
    conn = sqlite3.connect("db/db.db")
    cursor = conn.cursor()
    
    
    def get_with_id():
        sql = None
        user_id = retrieve_id()

        if element == "Question":
            sql = "SELECT * FROM questions WHERE UID = ?"
        if element == "Answer":
            sql = "SELECT * FROM answesr WHERE UID = ?"

        if user_id is not None:
            try:
                data = cursor.execute(sql, (user_id,)).fetchall()
                return data
            except sqlite3.Error as e:
                print(f'Error getting the question with id: {e}')
                return None
            finally:
                conn.close()
        else:
            return None
    
    def get_all():
        sql = None
        if element == "Question":
            sql = "SELECT * FROM questions LIMIT 50"
        if element == "Answer":
            sql = "SELECT * FROM answers LIMIT 50"

        try:
            data = cursor.execute(sql).fetchall()
            return data
        except sqlite3.Error as e:
            print(f'Error getting questions: {e}')
            return None
        finally:
            conn.close()
    
    if type == "all":
        return get_all()
    elif type == "with_id":
        return get_with_id()


def search_item(search_text, element):
    conn = sqlite3.connect("db/db.db")
    cursor = conn.cursor()

    sql = None
    if element == "Question":
        sql = "SELECT * FROM questions WHERE text LIKE ?"
    if element == "Answer":
        sql = "SELECT * FROM answers WHERE text LIKE ?"

    try:
        data = cursor.execute(sql, ('%' + search_text + '%',)).fetchall()
        return data
    except sqlite3.Error as e:
        print(f'Error searching: {e}')
        return None
    finally:
        conn.close()


""" #RELATED TO ANSWERS
def get_answers(type):
    conn = sqlite3.connect("db/db.db")
    cursor = conn.cursor()
    
    
    def get_with_id():
        user_id = retrieve_id()
        if user_id is not None:
            sql = "SELECT * FROM answers WHERE UID = ?"
            try:
                data = cursor.execute(sql, (user_id,)).fetchall()
                return data
            except sqlite3.Error as e:
                print(f'Error getting the answer with id: {e}')
                return None
            finally:
                conn.close()
        else:
            return None
    
    def get_all():
        sql = "SELECT * FROM answers LIMIT 50"
        try:
            data = cursor.execute(sql).fetchall()
            return data
        except sqlite3.Error as e:
            print(f'Error getting answers: {e}')
            return None
        finally:
            conn.close()
    
    if type == "all":
        return get_all()
    elif type == "with_id":
        return get_with_id()


def search_answers(search_text):
    conn = sqlite3.connect("db/db.db")
    cursor = conn.cursor()

    sql = "SELECT * FROM answers WHERE text LIKE ?"
    try:
        data = cursor.execute(sql, ('%' + search_text + '%',)).fetchall()
        return data
    except sqlite3.Error as e:
        print(f'Error searching: {e}')
        return None
    finally:
        conn.close()
 """

### ADDING STUFF
## ADD ELEMENT(QUESTION/ANSWER)
def add_element(text, element):
    conn = sqlite3.connect("db/db.db")
    cursor = conn.cursor()
    user_id = retrieve_id()
    id = str(uuid.uuid4())  # Generate a unique ID for element

    data = {"statusCode": ""}

    sql = None

    if element == "Question":
        sql = "INSERT INTO questions (text, UID, id) VALUES (?, ?, ?)"
    if element == "Answer":
        sql = "INSERT INTO answers (text, UID, id) VALUES (?, ?, ?)"

    if user_id is not None:
      try:
        cursor.execute(sql, (text, user_id, id))
        conn.commit()
        data["statusCode"] = 200
        return data
      except sqlite3.Error as e:
          print(f'Error adding {element}: {e}')
          data["statusCode"] = 501
          return data
      finally:
          conn.close()
    else:
        data["statusCode"] = 401
        return data


##ADD ANSWER
def add_answer(answer):
    conn = sqlite3.connect("db/db.db")
    cursor = conn.cursor()
    id = retrieve_id()
    data = {"statusCode": ""}

    sql = "INSERT INTO answers (text, UID) VALUES (?, ?)"

    if id is not None:
      try:
        cursor.execute(sql, (answer, id))
        conn.commit()
        data["statusCode"] = 200
        return data
      except sqlite3.Error as e:
          print(f'Error searching: {e}')
          data["statusCode"] = 501
          return data
      finally:
          conn.close()
    else:
        data["statusCode"] = 401
        return data


## EDITING STUFF
## UPDATE ELEMENT(QUESTION/ANSWER)
def update_element(question, id, element):
    conn = sqlite3.connect("db/db.db")
    cursor = conn.cursor()
    data = {"statusCode": ""}
    #print(f"the id is here: {id}")

    sql = None

    if element == "Question":
        sql = "UPDATE questions SET text = ? WHERE id = ?"
    if element == "Answer":
        sql = "UPDATE answers SET text = ? WHERE id = ?"
    
    try:
        cursor.execute(sql, (question, id))
        conn.commit()
        data["statusCode"] = 200
    except sqlite3.Error as e:
        print(f'Error updating element the {element}: {e}')
        data["statusCode"] = 500
    finally:
        conn.close()

    return data


## DELETE STUFF
## DELETE ELEMENT(QUESTION/ANSWER)
def destroy_element(id, element):
    conn = sqlite3.connect("db/db.db")
    cursor = conn.cursor()
    data = {"statusCode": ""}
    #print(f"the id is here delete: {id}")

    sql = None

    if element == "Question":
        sql = "DELETE FROM questions WHERE id = ?"
    if element == "Answer":
        sql = "DELETE FROM answers WHERE id = ?"

    try:
        cursor.execute(sql, (id,))
        conn.commit()
        data["statusCode"] = 200
    except sqlite3.Error as e:
        print(f'Error deleting element the {element}: {e}')
        data["statusCode"] = 500
    finally:
        conn.close()

    return data


