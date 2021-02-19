from flask import Flask
import mariadb
import json
import random
import dbcreds

app = Flask(__name__)

# animals=["Lion", "Tiger", "Wolf", "Snake", "Panda", "Scorpion", "Komodo Dragon"]

def connect():
      return mariadb.connect(
         user = dbcreds.user,
         password = dbcreds.password,
         host = dbcreds.host,
         port = dbcreds.port,
         database = dbcreds.database
    )

     
@app.route('/animals', methods = ['GET', 'POST', 'PATCH', 'DELETE'])
def animals():
    if request.method == 'GET':
        try:
            conn = connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM animals")
            result = cursor.fetchall()
            animals=[]
            for item in result:
                animal={"id" : item[0], "name" : item[1]
                    }
                animals.append(animal) 
        except mariadb.OperationalError as ex:
            print("Problem with connection", ex) 
        except:
            print("An error has occured") 
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close() 
                return Response(
                    json.dumps(animals, default=str),
                    mimetype="application/json",
                    status=200
                )                    
       
    elif request.method == 'POST':
        animal = request.json
        try:
            conn = connect()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO animals(name) VALUES (?)",[animal["name"]])
            conn.commit()
        except mariadb.OperationalError as ex:
            print("Problem connecting", ex)
        except:
            print("An error has occured")
        finally:
            if (cursor != None):
                cursor.close()
            if (conn != None):
                conn.rollback()
                conn.close()  
                return Response(
                    "Success",
                     mimetype="text/html",
                     status=201
                )



           
    elif request.method == 'PATCH':
        animal = request.json
        try:
            conn = connect()
            cursor = conn.cursor()
            cursor.execute("UPDATE animals SET name=? WHERE id = ?",[animal["name"], ["id"]])
            conn.commit()
        except mariadb.OperationalError as ex:
            print("Problem connecting", ex)
        except:
            print("An error has occured")    
        finally:
            if (cursor != None):
                cursor.close()
            if (cursor != None):
                conn.rollback()
                conn.close()
                return Response(
                    "Update success",
                     mimetype="text/html",
                     status=201
                )             
        
    elif request.method == 'DELETE':
        animal_id = request.json["id"]
        try:
            conn = connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM animals WHERE id=?", [animal_id])
            conn.commit()

        except mariadb.OperationalError as ex:
            print("Problme connecting", ex)
        except:
            print("An error has occured")
        finally:
            if (cursor != None):
                cursor.close()
            if (cursor != None):
                conn.rollback()
                conn.close() 
                return Response(
                     "Delete success",
                     mimetype="text/html",
                     status=203
                )                
         
   
