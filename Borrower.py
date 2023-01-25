import mysql.connector
from mysql.connector import errorcode
from datetime import datetime, timedelta
from tkinter import *
from tkinter import simpledialog, messagebox
from tkinter.ttk import Treeview
import re

from main import *
cnx = mysql.connector.connect(**{'user':'sqluser','password':'password','host':'localhost','db':'library'})


class Borrower:
    def __init__(self, master):
        self.parent = master

        self.titleLabel = Label(self.parent, text="Enter Details", fg="green", font= "Bold")
        self.titleLabel.grid(row=0, column=0, padx=20, pady=20, columnspan=2)

        self.fnameLabel = Label(self.parent, text="First Name").grid(row=1, column=0, padx=10, pady=5)
        self.fnameTB = Entry(self.parent)
        self.fnameTB.grid(row=2, column=0, padx=10, pady=5)

        self.lnameLabel = Label(self.parent, text="Last Name").grid(row=1, column=1, padx=10, pady=5)
        self.lnameTB = Entry(self.parent)
        self.lnameTB.grid(row=2, column=1, padx=10, pady=5)

        self.ssnLabel = Label(self.parent, text="SSN").grid(row=3, column=0, padx=10, pady=5)
        self.ssnTB = Entry(self.parent)
        self.ssnTB.grid(row=4, column=0, padx=10, pady=5)

        self.addressLabel = Label(self.parent, text="Street Address").grid(row=5, column=0, padx=10, pady=5)
        self.addressTB = Entry(self.parent)
        self.addressTB.grid(row=6, column=0, padx=10, pady=5)

        self.cityLabel = Label(self.parent, text="City").grid(row=5, column=1, padx=10, pady=5)
        self.cityTB = Entry(self.parent)
        self.cityTB.grid(row=6, column=1, padx=10, pady=5)

        self.stateLabel = Label(self.parent, text="State").grid(row=7, column=0, padx=10, pady=5)
        self.stateTB = Entry(self.parent)
        self.stateTB.grid(row=8, column=0, padx=10, pady=5)

        self.numberLabel = Label(self.parent, text="Phone Number").grid(row=3, column=1, padx=10, pady=5)
        self.numberTB = Entry(self.parent)
        self.numberTB.grid(row=4, column=1, padx=10, pady=5)

        self.emailLabel = Label(self.parent, text="Email").grid(row=7, column=1, padx=10, pady=5)
        self.emailLabelTB = Entry(self.parent)
        self.emailLabelTB.grid(row=8, column=1, padx=10, pady=5)

        self.addBtn = Button(self.parent, text="Add", command=self.add_borrower, background="brown", fg="white")
        self.addBtn.grid(row=9, column=0, padx=10, pady=5, columnspan=2)

    def add_borrower(self):
        ssn = self.ssnTB.get()
        cursor = cnx.cursor()
        cursor.execute("SELECT MAX(Card_id) from BORROWER")
        borrower_id = (cursor.fetchall()[0][0])[2:]
        new_card = int(borrower_id) + 1
        new_card_no = "ID"+((str(new_card)).zfill(6))
        email = self.emailLabelTB.get()
        if len(self.fnameTB.get()) == 0 or len(self.lnameTB.get()) == 0 or not self.fnameTB.get().isalpha or not self.lnameTB.get().isalpha:
                self.fnameTB.delete(0,END)
                self.lnameTB.delete(0,END)
                messagebox.showerror("Validation Error", "Enter correct Name!")
                return None

        if len(ssn) != 9 or ssn.isdigit() == False:
            self.ssnTB.delete(0,END)
            messagebox.showerror("Validation Error", "Enter correct value of SSN!")
            return None

        if len(self.numberTB.get()) != 10 or ssn.isdigit() == False:
            self.numberTB.delete(0,END)
            messagebox.showerror("Validation Error", "Enter correct Phone Number")
            return None

        if len(self.addressTB.get())==0 or len(self.cityTB.get())==0 or len(self.stateTB.get())==0 or not self.addressTB.get().isalnum or not self.cityTB.get().isalpha or not self.stateTB.get().isalpha:
            self.addressTB.delete(0,END)
            self.cityTB.delete(0,END)
            self.stateTB.delete(0,END)
            messagebox.showerror("Validation Error", "Enter correct Address")
            return None

        if len(email)!=0:
            pat = r'\b[A-Za-z0-9._-]+@[A-Za-z,-]+\.[A-Z|a-z]{2,}\b'
            if re.match(pat,email):
                print("Valid Email")
            else:
                messagebox.showinfo("Error","Please enter a valid Email")
                return None

        ssn = str(ssn)[0:3]+"-"+str(ssn)[3:5]+"-"+str(ssn)[5:]
        cursor.execute("SELECT EXISTS(SELECT Ssn FROM BORROWER WHERE BORROWER.ssn = '" + str(ssn) + "')")
        result = cursor.fetchall()
        if result == [(0,)]:
            cursor.execute("Insert into BORROWER (Card_id, ssn, first_name, last_name, email, address, city, state, phone) Values ('" + new_card_no + "', '" + ssn + "', '" + str(self.fnameTB.get()) + "', '" + str(self.lnameTB.get()) + "','" + str(self.emailLabelTB.get()) + "', '" + str(self.addressTB.get()) + "', '" + str(self.cityTB.get()) + "', '" + str(self.stateTB.get()) + "','" + str(self.numberTB.get()) + "')")
            cnx.commit()
            self.parent.destroy()
            messagebox.showinfo("Success", "Borrower has been added successfully!")
        else:
            messagebox.showinfo("Error", "Borrower Already Exists!")