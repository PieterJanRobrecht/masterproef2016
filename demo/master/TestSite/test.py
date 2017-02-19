from Tkinter import *
import mysql.connector


def connect_to_db():
    cnx = mysql.connector.connect(user='root', password='root',
                                  host='127.0.0.1',
                                  database='mydb')

    cursor = cnx.cursor(dictionary=True)
    return cursor, cnx

cursor, cnx = connect_to_db()
query = "SELECT * FROM installer"
cursor.execute(query)
print type(cursor)
for row in cursor:
    print row['name']
cnx.close()


def button_click(event):
    print("click")


root = Tk()
topFrame = Frame(root)
topFrame.pack()

bottomFrame = Frame(root)
bottomFrame.pack(side=BOTTOM)

label = Label(bottomFrame, text="Test")
label.pack()

button = Button(topFrame, text="Ik ben een button")
button.bind("<Button-1>", func=button_click)
button.pack(side=RIGHT)

root.mainloop()
