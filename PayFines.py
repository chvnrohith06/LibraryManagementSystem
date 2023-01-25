import mysql.connector
from mysql.connector import errorcode
from datetime import datetime, timedelta
from tkinter import *
from tkinter import simpledialog, messagebox
from tkinter.ttk import Treeview

from main import *
cnx = mysql.connector.connect(**{'user':'sqluser','password':'password','host':'localhost','db':'library'})
todays_date = datetime.today()

class PayFines:
    def __init__(self, master):
        self.parent = master

        self.v = StringVar()

        self.bookForCheckInID = None
        self.search_string = None
        self.data = None

        self.searchLabel = Label(self.parent, text="Enter Borrower ID here!")
        self.searchLabel.grid(row=0, column=0, padx=20, pady=20)
        self.borrowerEntry = Entry(self.parent, width=50)
        self.borrowerEntry.grid(row=1, column=0)
        self.searchBtn = Button(self.parent, text="Show Fines", command=self.search_book_loans, background="green", fg="white")
        self.searchBtn.grid(row=2, column=0, pady = 5)
        self.table = Treeview(self.parent, columns=["loan_id","ISBN", "Title","Fin_amt", "Pay_status","Ret_status"])
        self.table.grid(row=3, column=0)
        self.table.heading('#0', text="Loan Id")
        self.table.heading('#1', text="ISBN")
        self.table.heading('#2', text="Book Title")
        self.table.heading('#3', text="Fine Amount")
        self.table.heading('#4', text="Return Status")
        self.table.heading('#5', text="Payment Status")
        self.table.bind('<ButtonRelease-1>', self.select_book_for_checkin)
        self.checkInBtn = Button(self.parent, text="Pay Fine", command=self.pay_fine, background="brown", fg="white")
        self.checkInBtn.grid(row=5, column=0, pady= 5)

        self.fineLabel = Label(self.parent, textvariable=self.v)
        self.fineLabel.grid(row=4, column=0, padx=20, pady=20)
    
    def search_book_loans(self):
        self.borrowe_id = self.borrowerEntry.get()
        cursor = cnx.cursor()
        cursor.execute("SELECT fines.loan_id,book_loans.Isbn,books.Title,fines.fine_amt,book_loans.date_in, case when fines.paid=1 then 'Paid' else 'Not Paid' END as fine_status, book_loans.due_date "
                        "FROM BOOK_LOANS join BOOKs ON BOOKS.Isbn = BOOK_LOANS.Isbn join FINES ON FINES.LOAN_ID = BOOK_LOANS.LOAN_ID"
                        " where BOOK_LOANS.Card_id like concat('" + self.borrowe_id + "')")

        self.data = cursor.fetchall()
        self.view_data()
        self.show_fines()

    def view_data(self):
        self.table.delete(*self.table.get_children())
        for elem in self.data:
            if elem[4] is not None:
                diff = elem[6]-elem[4]
            else:
                diff = (elem[6]-todays_date.date())
            
            if diff.days < 0:
                        self.table.insert('', 'end', text=str(elem[0]), values=(elem[1], elem[2], elem[3], elem[4],elem[5]))


    def select_book_for_checkin(self, a):
        curItem = self.table.focus()
        self.bookForCheckInID = self.table.item(curItem)['text']
        
    def show_fines(self):
        cursor = cnx.cursor()
        cursor.execute("SELECT EXISTS(SELECT Card_id FROM BORROWER WHERE BORROWER.Card_id = '" + str(self.borrowerEntry.get()) + "')")
        result = cursor.fetchall()
        total_fine = 0

        if result == [(0,)]:
            messagebox.showinfo("Error", "Borrower does not exist in data")
        else:
            cursor.execute("SELECT FINES.fine_amt, FINES.paid FROM FINES JOIN BOOK_LOANS ON FINES.Loan_Id = BOOK_LOANS.Loan_Id WHERE BOOK_LOANS.Card_id = '" + str(self.borrowerEntry.get()) + "'")
            result = cursor.fetchall()
            total_fine = 0
            for elem in result:
                if elem[1] == 0:
                    total_fine += float(elem[0])
        fine_t = format(total_fine, '.2f')
        self.v.set("Fine: $ " + str(fine_t))

    def pay_fine(self):
        if self.bookForCheckInID is None:
            messagebox.showinfo("Attention!", "Select Book to Pay Fine!")
            return None
        borrower_id = self.borrowerEntry.get()
        cursor = cnx.cursor()
        cursor.execute(
            "SELECT EXISTS(SELECT Card_id FROM BORROWER WHERE BORROWER.Card_id = '" + str(borrower_id) + "')")
        result = cursor.fetchall()
        if result == [(0,)]:
            messagebox.showinfo("Error", "Borrower does not exist in data")
        else:
            cursor = cnx.cursor()
           
            cursor.execute("SELECT BOOK_LOANS.Date_in FROM BOOK_LOANS WHERE BOOK_LOANS.Loan_Id = '" + str(self.bookForCheckInID) + "'")
            result = cursor.fetchall()
            if(result[0][0]!= None):
                cursor = cnx.cursor()
                cursor.execute("UPDATE FINES SET FINES.paid = 1 WHERE FINES.Loan_Id = '" + str(self.bookForCheckInID) + "'")
                cnx.commit()
                messagebox.showinfo("Info", "Fines Paid!")
            else:
                messagebox.showinfo("Alert", "Return the book before paying the due")
                return None     
            self.parent.destroy()