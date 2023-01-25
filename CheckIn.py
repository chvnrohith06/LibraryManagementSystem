import mysql.connector
from mysql.connector import errorcode
from datetime import datetime, timedelta
from tkinter import *
from tkinter import simpledialog, messagebox
from tkinter.ttk import Treeview

from main import *
cnx = mysql.connector.connect(**{'user':'sqluser','password':'password','host':'127.0.0.1','db':'library'})

class CheckIn:
    def __init__(self, master):
        self.parent = master

        self.bookForCheckInID = None
        self.search_string = None
        self.data = None

        self.searchLabel = Label(self.parent, text="Enter Borrower ID or Borrower Name or ISBN here...")
        self.searchLabel.grid(row=0, column=0, padx=20, pady=20)
        self.searchTextBox = Entry(self.parent, width=50)
        self.searchTextBox.grid(row=1, column=0)
        self.searchBtn = Button(self.parent, text="Search", command=self.search_book_loans, background="green", fg="white")
        self.searchBtn.grid(row=2, column=0, pady = 5)
        self.table = Treeview(self.parent, columns=["Loan ID", "ISBN", "Borrower ID", "Title"])
        self.table.grid(row=3, column=0)
        self.table.heading('#0', text="Loan ID")
        self.table.heading('#1', text="ISBN")
        self.table.heading('#2', text="Borrower ID")
        self.table.heading('#3', text="Book Title")
        self.table.bind('<ButtonRelease-1>', self.select_book_for_checkin)
        self.checkInBtn = Button(self.parent, text="Check In", command=self.check_in, background="brown", fg="white")
        self.checkInBtn.grid(row=4, column=0, pady= 5)

    def search_book_loans(self):
        self.search_string = self.searchTextBox.get()
        cursor = cnx.cursor()
        cursor.execute("select BOOK_LOANS.Loan_Id, BOOK_LOANS.ISBN, BOOK_LOANS.Card_id, BOOKS.title, BOOK_LOANS.Date_in from BOOK_LOANS "
                       "join BORROWER on BOOK_LOANS.Card_id = BORROWER.Card_id "
                       "join BOOKS on BOOK_LOANS.ISBN = BOOKS.ISBN "
                       "where BOOK_LOANS.ISBN like concat('%', '" + self.search_string + "', '%') or "
                        "BORROWER.first_name like concat('%', '" + self.search_string + "', '%') or "
                        "BORROWER.last_name like concat('%', '" + self.search_string + "', '%') or "
                        "BOOK_LOANS.Card_id like concat('%', '" + self.search_string + "', '%')")

        self.data = cursor.fetchall()
        self.view_data()

    def view_data(self):
        self.table.delete(*self.table.get_children())
        for elem in self.data:
            if elem[4] is None:
                self.table.insert('', 'end', text=str(elem[0]), values=(elem[1], elem[2], elem[3]))

    def select_book_for_checkin(self, a):
        curItem = self.table.focus()
        self.bookForCheckInID = self.table.item(curItem)['text']

    def check_in(self):
        todays_date = datetime.today()
        if self.bookForCheckInID is None:
            messagebox.showinfo("Attention!", "Select Book to Check In First!")
            return None
        cursor = cnx.cursor()
        cursor.execute("SELECT BOOK_LOANS.Date_in FROM BOOK_LOANS WHERE BOOK_LOANS.Loan_Id = '" + str(self.bookForCheckInID) + "'")
        result = cursor.fetchall()
        if result[0][0] is None:
            cursor.execute("UPDATE BOOK_LOANS SET BOOK_LOANS.Date_in = '" + str(todays_date) + "' WHERE BOOK_LOANS.Loan_Id = '"
                           + str(self.bookForCheckInID) + "'")
            cnx.commit()
            messagebox.showinfo("Done", "Book Checked In Successfully!")
            self.parent.destroy()
        else:
            return None

