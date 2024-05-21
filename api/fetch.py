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


## LOGIN USER
def login_user(email, password):
    conn = sqlite3.connect("db/db.db")
    cursor = conn.cursor()
    data = {"statusCode": ""}

    try:
        # the code
        sql = "SELECT id, name, email, password FROM users WHERE email = ?"
        cursor.execute(sql, (email,))
        user = cursor.fetchone()

        if not user:
            data["statusCode"] = 404
        elif bcrypt.checkpw(password.encode("utf-8"), user[3]):
            #print(f'user: {str(user)}')
            store_data(user)
            data["statusCode"] = 200
        else:
            data["statusCode"] = 301
    except sqlite3.Error as e:
        #the code
        data["statusCode"] = 501
        print(f"Error: {str(e)}")

    return data



## RELATED TO QUESTIONS
def get_item(type, element):
    conn = sqlite3.connect("db/db.db")
    cursor = conn.cursor()

    user_id = retrieve_data()["userID"]
    if not user_id: return {"statusCode": "401"}
    
    def get_with_id():
        sql = None
        

        if element == "Question":
            sql = "SELECT * FROM questions WHERE UID = ?"
        if element == "Answer":
            sql = "SELECT * FROM answers WHERE UID = ?"

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


## SEARCH ITEM
def search_item(search_text, element):
    conn = sqlite3.connect("db/db.db")
    cursor = conn.cursor()

    if not retrieve_data()["userID"]: return {"statusCode": "401"}

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


### ADDING STUFF
## ADD ELEMENT(QUESTION/ANSWER)
def add_element(text, element):
    conn = sqlite3.connect("db/db.db")
    cursor = conn.cursor()
    user_id = retrieve_data()["userID"]
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


## EDITING STUFF
## UPDATE ELEMENT(QUESTION/ANSWER)
def update_element(question, id, element):
    conn = sqlite3.connect("db/db.db")
    cursor = conn.cursor()
    data = {"statusCode": ""}
    #print(f"the id is here: {id}")

    if not retrieve_data()["userID"]: return {"statusCode": "401"}

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
        data["statusCode"] = 501
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

    if not retrieve_data()["userID"]: return {"statusCode": "401"}

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
        data["statusCode"] = 501
    finally:
        conn.close()

    return data


## UPDATE PASSWORD
def update_password(newPassword, oldPassword):
    conn = sqlite3.connect("db/db.db")
    cur = conn.cursor()
    data = retrieve_data()
    response = {"statusCode": ""}

    sql = "SELECT password FROM users WHERE email = ?"

    try:
        cur.execute(sql, (data["email"],))
        user = cur.fetchone()

        if bcrypt.checkpw(oldPassword.encode("utf-8"), user[0]):
            userConfirm = shop_popup("Dikkat", "Şifrenizi değiştirmek istediğinizden emin misiniz ?", "warning", True)

            if userConfirm == "OK":  # Check if the user confirmed with "OK"
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(newPassword.encode('utf-8'), salt) #Hash the password
                sql = "UPDATE users SET password = ? WHERE email = ? AND id = ?"

                try:
                    cur.execute(sql, (hashed_password, data["email"], data["userID"]))
                    conn.commit()
                    response["statusCode"] = 200
                except sqlite3.Error as e:
                    response["statusCode"] = 501
        else:
            response["statusCode"] = 401  # Old password does not match
    except sqlite3.Error as e:
        print(f'Internal error encounterd: {e}')
        data["statusCode"] = 501
    
    return response


## UPDATE PASSWORD
def update_name(name):
    conn = sqlite3.connect("db/db.db")
    cur = conn.cursor()
    data = retrieve_data()
    response = {"statusCode": ""}


    sql = "UPDATE users SET name = ? WHERE email = ? AND id = ?"

    userConfirm = shop_popup("Dikkat", "Adınızı değiştirmek istediğinizden emin misiniz ?", "warning", True)

    if userConfirm == "OK":  # Check if the user confirmed with "OK"
        try:
            cur.execute(sql, (name, data["email"], data["userID"]))
            conn.commit()

            #Change the stored data
            updatedData = [data["userID"], name, data["email"]]
            store_data(updatedData)
            response["statusCode"] = 200
        except sqlite3.Error as e:
            print(f'Internal error encounterd: {e}')
            response["statusCode"] = 501
        finally:
            conn.close()  # Ensure the connection is closed
    return response

