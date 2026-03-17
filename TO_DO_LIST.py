import mysql.connector
from tkinter import *
from tkinter import messagebox

root = Tk()
root.title("To Do List")
root.geometry("800x600")

def connection():

    task = entry.get() 

    if task == "":
        messagebox.showwarning("Input Error", "Please enter a task.")
        return

    try:
        conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = ""
        )
        cursorObject = conn.cursor()

        cursorObject.execute("CREATE DATABASE IF NOT EXISTS To_Do_List")

        cursorObject.execute("USE To_Do_List")

        List = """CREATE TABLE IF NOT EXISTS Tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            task VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            deleted_at TIMESTAMP NULL
            )"""

        cursorObject.execute(List)
        insert_query = "INSERT INTO Tasks (task) VALUES (%s)"
        cursorObject.execute(insert_query, (task,))
        conn.commit()
  
        entry.delete(0, END) 

        load_task()


    except mysql.connector.Error as error:
        messagebox.showwarning(f"Database Update Failed! Error: {error}")
         

def load_task():

    try:
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "To_Do_List"
            )
        cursorObject = conn.cursor()
        cursorObject.execute("SELECT id, task FROM Tasks")
        tasks = cursorObject.fetchall()  

        listbox.delete(0, END)
        for task in tasks:
            listbox.insert(END, f"{task[0]} - {task[1]}")

    except mysql.connector.Error as error:
        messagebox.showwarning(f"Database Load Failed! Error: {error}")


def delete_task():
    Selected = listbox.curselection()
    if not Selected:
        messagebox.showwarning("Selection Error", "Please select a task to delete.")
        return
    
    task_id = listbox.get(Selected[0]).split(" - ")[0]
    try:
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "To_Do_List"
            )
        cursorObject = conn.cursor()
        delete_query = "DELETE FROM Tasks WHERE id = %s"
        cursorObject.execute(delete_query, (task_id,))
        conn.commit()
        conn.close()

        listbox.delete(Selected[0])

    except mysql.connector.Error as error:
        messagebox.showwarning(f"Database Deletion Failed! Error: {error}")
        return
    

entry = Entry(root, font=("Arial", 24), relief= 'flat', borderwidth=10, highlightbackground="black", highlightthickness=2)
entry.place(x=5, y=5)

btn =  Button(root, text="Add", font=('new times roman',18), relief='raised', command=connection)
btn.place (x =  400 , y = 10,height=50, width=100  )

btn =  Button(root, text="Delete", font=('new times roman',18), relief='raised', command=delete_task)
btn.place (x =  500 , y = 10,height=50, width=100  )

btn =  Button(root, text="Load", font=('new times roman',18), relief='raised', command=load_task)
btn.place (x =  600 , y = 10,height=50, width=100  )

listbox = Listbox(root, font=("Arial", 20), relief='flat', borderwidth=10, highlightbackground="black", highlightthickness=2)
listbox.place(x=5, y=80, height=500, width=790)

scrollbar = Scrollbar(root)
scrollbar.place(x=770, y=80, height=500)

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)


root.mainloop()