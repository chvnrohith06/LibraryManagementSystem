import mysql.connector
from mysql.connector import errorcode
from datetime import datetime, timedelta
from tkinter import *
from tkinter import simpledialog, messagebox
from tkinter.ttk import Treeview
import tkinter.ttk as ttk
from ttkthemes import ThemedTk


from LibraryGUI import *
from PayFines import *
from Borrower import *
from CheckIn import *

cnx = mysql.connector.connect(**{'user':'sqluser','password':'password','host':'localhost','db':'library'})
cursor = None
todays_date = datetime.today()

if __name__ == '__main__':
    root = ThemedTk(theme="radiance")
    tool = LibraryGUI(root)
    root.mainloop()
