from utils.generalFunctions import *
import sqlite3

## RELATED TO QUESTIONS
def get_questions(type):
    conn = sqlite3.connect("db/db.db")
    cursor = conn.cursor()
    
    
    def get_with_id():
        user_id = retrieve_id()
        if user_id is not None:
            sql = "SELECT * FROM questions WHERE UID = ?"
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
        sql = "SELECT * FROM questions LIMIT 50"
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



def search_questions(search_text):
    conn = sqlite3.connect("db/db.db")
    cursor = conn.cursor()

    sql = "SELECT * FROM questions WHERE text LIKE ?"
    try:
        data = cursor.execute(sql, ('%' + search_text + '%',)).fetchall()
        return data
    except sqlite3.Error as e:
        print(f'Error searching: {e}')
        return None
    finally:
        conn.close()


#RELATED TO ANSWERS
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


### ADDING STUFF

##ADD QUESTION
def add_question(question):
    conn = sqlite3.connect("db/db.db")
    cursor = conn.cursor()
    id = retrieve_id()
    data = {"statusCode": ""}

    sql = "INSERT INTO questions (text, UID) VALUES (?, ?)"

    if id is not None:
      try:
        cursor.execute(sql, (question, id))
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

## UPDATE QUESTION
def update_question(question, id):
    conn = sqlite3.connect("db/db.db")
    cursor = conn.cursor()
    data = {"statusCode": ""}
    print(f"the id is here: {id}")

    sql = "UPDATE questions SET text = ? WHERE id = ?"
    try:
        cursor.execute(sql, (question, id))
        conn.commit()
        data["statusCode"] = 200
    except sqlite3.Error as e:
        print(f'Error updating question: {e}')
        data["statusCode"] = 500
    finally:
        conn.close()

    return data


## UPDATE ANSWER
def update_answer(question, id):
    conn = sqlite3.connect("db/db.db")
    cursor = conn.cursor()
    data = {"statusCode": ""}
    print(f"the id is here: {id}")

    sql = "UPDATE answers SET text = ? WHERE id = ?"

    try:
        cursor.execute(sql, (question, id))
        conn.commit()
        data["statusCode"] = 200
    except sqlite3.Error as e:
        print(f'Error updating answer: {e}')
        data["statusCode"] = 500
    finally:
        conn.close()

    return data

## DELETE STUFF
## Deleting question
def destroy_question(id):
    conn = sqlite3.connect("db/db.db")
    cursor = conn.cursor()
    data = {"statusCode": ""}
    print(f"the id is here delete: {id}")

    sql = "DELETE FROM questions WHERE id = ?"

    try:
        cursor.execute(sql, (id,))
        conn.commit()
        data["statusCode"] = 200
    except sqlite3.Error as e:
        print(f'Error deleting question: {e}')
        data["statusCode"] = 500
    finally:
        conn.close()

    return data


## Deleting answer
def destroy_answer(id):
    conn = sqlite3.connect("db/db.db")
    cursor = conn.cursor()
    data = {"statusCode": ""}
    print(f"the id is here: {id}")

    sql = "DELETE FROM answers WHERE id = ?"

    try:
        cursor.execute(sql, (id,))
        conn.commit()
        data["statusCode"] = 200
    except sqlite3.Error as e:
        print(f'Error deleting answer: {e}')
        data["statusCode"] = 500
    finally:
        conn.close()

    return data
