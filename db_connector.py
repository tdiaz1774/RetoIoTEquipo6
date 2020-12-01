import os
import sys
import sqlite3
from sqlite3 import Error
from datetime import datetime
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def findUser(number):
    """ Finds if user exists in the data base.
    findUser(number: str) -> bool, str
    It can return true and the name of the user or false and "nouserfound".
    """
    
    con = sqlite3.connect('mydatabase.db')
    cursorObj = con.cursor()

    try:
        sql = 'select * from Paciente where numero="%s"' % (number)
        cursorObj.execute(sql)
        rows = cursorObj.fetchall()
        for row in rows:
            return True, row[1]

    except Exception as err:
        print("User does not exist in data base")
        print(f"Error: {e}")
        return False, "nouserfound"


#print(find_user("whatsapp:+525514200581"))

def insertHR(number, data):
    """Insert Heart Rate into database.
    insertHR(number: int, data: int)
    """

    con = sqlite3.connect('mydatabase.db')
    cursorObj = con.cursor()
    sql = f'insert into HeartRate ("id","Numero","Data","Fecha","id_paciente") VALUES (NULL, "{number}","{data}","{datetime.now().strftime("%d/%m/%Y %H")}","{number}");'
    print(f"Data inserted into HeartRate -> {data}")
    cursorObj.execute(sql)
    con.commit()
    con.close()

def createImg(number, type):

    con = sqlite3.connect('mydatabase.db')
    cursorObj = con.cursor()

    if type == "HR":
        sql = 'select * from HeartRate where Numero="%s"' % (number)
        print("Getting Heart Rate")
        cursorObj.execute(sql)
        rows = cursorObj.fetchall()
    elif type == "Spo2":
        sql = 'select * from Spo2 where Numero="%s"' % (number)
        print("Getting Spo2")
        cursorObj.execute(sql)
        rows = cursorObj.fetchall()

    con.close()

    x = []
    y = []

    for item in rows:    
        # Este es el orden para seleccionar los datos en la iteración de [rows]
        # 0 -> id, 1 -> Numero, 2 -> Data, 3 -> Fecha, 4 -> id_paciente
        x.append(item[3])
        y.append(item[2])

    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set(xlabel='Fecha de consulta', ylabel='HR', title='Heart Rate Graph')
    ax.grid()
    fig.savefig(number.replace(":","_")+".png")
    return

createImg("1", "HR")


def checkDataBase():
    """ Checks if the data base exists.
    db_check() -> bool
    """
    if os.path.isfile('mydatabase.db'):          
        return True
    return False


def createDataBase():
    """ Creates a data base.
    """

    if os.path.isfile('mydatabase.db'):
        return

    print("Primero deberas registrar tus datos \n")

    print("Escribe tu numero celular: ", end="")        
    numero = "whatsapp:+521" + input()

    print("Escribe tu nombre: ", end="")
    nombre = input()

    print("Escribe tu apellido: ", end="")
    apellido = input()

    print("Escribe tu e-mail: ", end="")
    email = input()

    con = sqlite3.connect('mydatabase.db')
    cursorObj = con.cursor()

    sql = "CREATE TABLE Paciente ( Numero text PRIMARY KEY, Nombre text, Apellido text, Email text)"
    cursorObj.execute(sql)
    print("tabla paciente -> ok")

    sql = f'INSERT INTO Paciente (Numero, Nombre, Apellido, Email) VALUES ("{numero}","{nombre}","{apellido}","{email}")'
    cursorObj.execute(sql)
    print("Usuario registrado")

    sql = "CREATE TABLE HeartRate ( id INTEGER PRIMARY KEY AUTOINCREMENT, Numero text, Data text, Fecha text, id_paciente text , CONSTRAINT fk_id_paciente FOREIGN KEY(id_paciente) REFERENCES Paciente (Numero))"
    cursorObj.execute(sql)
    print("Tabla HeartRate -> ok")

    sql = "CREATE TABLE Spo2 ( id INTEGER PRIMARY KEY AUTOINCREMENT, Numero text , Data text, Fecha text, id_paciente text , CONSTRAINT fk_id_paciente FOREIGN KEY(id_paciente) REFERENCES Paciente (Numero))"
    cursorObj.execute(sql)
    print("Tabla Spo2 -> ok")

    con.commit()
    con.close()

