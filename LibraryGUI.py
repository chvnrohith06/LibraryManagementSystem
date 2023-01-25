import mysql.connector
from mysql.connector import errorcode
from datetime import datetime, timedelta
from tkinter import *
from tkinter import simpledialog, messagebox
from tkinter.ttk import Treeview
from PIL import ImageTk, Image



from main import *
cnx = mysql.connector.connect(**{'user':'sqluser','password':'password','host':'localhost','db':'library'})
#new_cnx = mysql.connector.connect(**{'user':'sqluser','password':'password','host':'localhost','db':'library'})

todays_date = datetime.today()
class LibraryGUI:
    def __init__(self, master):
        self.parent = master
        # Set frame for the whole thing
        #self.parent.geometry("1000x1000")
        self.parent.title("Library Management System")
        img = Image.open("C:/Users/vxc210001/Desktop/Dummy-Library-master main code/Dummy-Library-master/library.jpg")
        resized = img.resize((500, 500),Image.ANTIALIAS)
        photoimage = ImageTk.PhotoImage(resized)
        
        self.imageFrame = Frame(self.parent, width=1000, height=1200, background="white")
        self.imageFrame.grid(row=0, column=0)

        #Label for the searchbox
        self.imageLabel = Label(self.imageFrame, image = photoimage)
        self.imageLabel.image = photoimage
        self.imageLabel.grid(padx=10, pady=10)
        self.imageLabel.grid_rowconfigure(0, weight=0)
        self.imageLabel.grid_columnconfigure(0, weight=0)

        self.imagetextLabel1 = Label(self.imageLabel, text = '')
        self.imagetextLabel1.grid(row=0, column=1,padx=1, pady=1)
        self.imagetextLabel1.grid_rowconfigure(0, weight=1)
        self.imagetextLabel1.grid_columnconfigure(0, weight=1)
        #self.imagetextLabel1.grid_forget()

        self.imagetextLabel2 = Label(self.imageLabel, text = "Library Management System")
        self.imagetextLabel2.grid(row=1, column=1,padx=10, pady=10)
        self.imagetextLabel2.grid_rowconfigure(0, weight=1)
        self.imagetextLabel2.grid_columnconfigure(0, weight=1)

        self.imagetextLabel3 = Label(self.imageLabel, text = '')
        self.imagetextLabel3.grid(row=2, column=1,padx=1, pady=1)
        self.imagetextLabel3.grid_rowconfigure(0, weight=1)
        self.imagetextLabel3.grid_columnconfigure(0, weight=1)

        self.mainFrame = Frame(self.imageFrame, width=1000, height=400, background="lightgray")
        self.mainFrame.place(anchor='center', relx=0.5, rely=1)
        self.mainFrame.grid(row=1, column=0)
        self.mainFrame.grid_rowconfigure(0, weight=1)
        self.mainFrame.grid_columnconfigure(0, weight=1)
        self.mainFrame.grid_propagate(False)
        
        self.search_string = None
        self.data = None
        self.borrowerId = None
        self.bookForCheckOutIsbn = None

        self.functions = Frame(self.mainFrame)
        self.functions.grid(row=0, column=0, sticky=N, pady=5)
        self.functions.grid_rowconfigure(0, weight=1)

        self.checkOutBtn = Button(self.functions, text="Check-Out", command=self.check_out)
        self.checkOutBtn.grid(row=0, column=0, padx=5, pady=10)
        self.checkOutBtn.grid_rowconfigure(0, weight=1)
        self.checkOutBtn.grid_columnconfigure(0, weight=1)

        self.checkInBtn = Button(self.functions, text="Check-In", command=self.check_in)
        self.checkInBtn.grid(row=0, column=1, padx=5, pady=10)
        self.checkOutBtn.grid_rowconfigure(0, weight=1)
        self.checkOutBtn.grid_columnconfigure(1, weight=1)

        self.updateFinesBtn = Button(self.functions, text="Refresh/Update Fines", command=self.update_fines)
        self.updateFinesBtn.grid(row=0, column=2, padx=5, pady=10)

        self.payFinesBtn = Button(self.functions, text="Pay Fine", command=self.pay_fines)
        self.payFinesBtn.grid(row=0, column=3, padx=5, pady=10)

        self.changeDayBtn = Button(self.functions, text="Change Day", command=self.change_day)
        self.changeDayBtn.grid(row=0, column=4, padx=5, pady=10)
        self.changeDayBtn.grid_forget()

        self.addBorrowerBtn = Button(self.functions, text="Add New Borrower", command=self.add_borrower)
        self.addBorrowerBtn.grid(row=0, column=5, padx=5, pady=10)



        # Search Frame
        self.SearchFrame = Frame(self.mainFrame)
        self.SearchFrame.grid(row=1, column=0)
        self.SearchFrame.grid_rowconfigure(1, weight=1)
        #If Author is searched in the input string then it should be given in the format - (;;Author_name)
        #If Title and Author is searched in the input string then it should be given in the format - (;Title;Author_name)
        #If ISBN, Title and Author is searched in the input string then it should be given in the format - (ISBN;Title;Author_name)
        #If Title is searched in the input string then it should be given in the format - (;Title)
        #If ISBN is searched in the input string then it should be given in the format - (ISBN)
        #If ISBN and Author is searched in the input string then it should be given in the format - (ISBN;;Author_name)
        #If ISBN and Title is searched in the input string then it should be given in the format - (ISBN;Title)

        self.SearchLabel = Label(self.SearchFrame, text='Enter search string here...(Input Format:ISBN;Title;Author):') 
        self.SearchLabel.grid(row=0, column=0, sticky=NW)
        self.SearchLabel.grid_rowconfigure(0, weight=1)

        self.searchText = Entry(self.SearchFrame, width=70)
        self.searchText.grid(row=1, column=0)
        self.searchText.grid_rowconfigure(1, weight=1)

        self.SearchButton = Button(self.SearchFrame, text='Search', background="green", fg="white", command=self.search)
        self.SearchButton.grid(row=1, column=1, columnspan=2, padx=2)

        # Search Result 
        self.ActiveArea = Frame(self.mainFrame)
        self.ActiveArea.grid(row=2, column=0, sticky=N, pady=8, padx=5)
        self.ActiveArea.grid_rowconfigure(2, weight=1)
        self.ActiveArea.grid_columnconfigure(4, weight=1)
        
        self.ResultTreeview = Treeview(self.ActiveArea, columns=["ISBN", "Book Title", "Author(s)", "Availability", "doa"])
        self.ResultTreeview.grid(row=1, column=1)
        self.ResultTreeview.grid_rowconfigure(0, weight=1)
        self.ResultTreeview.heading('#0', text="ISBN")
        self.ResultTreeview.heading('#1', text="Book Title")
        self.ResultTreeview.heading('#2', text="Author(s)")
        self.ResultTreeview.heading('#3', text="Availability")
        self.ResultTreeview.heading('#4', text="Date of Availability")
        self.ResultTreeview.bind('<ButtonRelease-1>', self.selectBookForCheckout)

    def change_day(self):
        global todays_date
        todays_date = todays_date + timedelta(days=1)
        print(todays_date)

    def search(self):
        temp = self.searchText.get().split(';')
        if(len(temp)==3):
            search_isbn = temp[0].strip()
            search_title = temp[1].strip()
            search_author = temp[2].strip()
        elif(len(temp)==2):
            search_isbn = temp[0].strip()
            search_title = temp[1].strip()
            search_author = ''
        elif(len(temp)==1):
            search_isbn = temp[0].strip()
            search_title = ''
            search_author = ''
        else:
            search_isbn = ''
            search_title = ''
            search_author = ''

        query1 = "select BOOKS.isbn, BOOKS.title, group_concat(AUTHORS.name) from BOOKS join BOOK_AUTHORS on BOOKS.isbn = BOOK_AUTHORS.isbn join AUTHORS on BOOK_AUTHORS.author_id = AUTHORS.author_id where"
        if(search_title==''):
            query2 =  ""
        else:
            query2 =  " BOOKS.title like concat('%', '" + search_title + "', '%')  "

        if(search_author==''):
            query3 =  ""
        else:
            query3 =  " AUTHORS.name like concat('%', '" + search_author + "', '%') "
        
        if(search_isbn==''):
            query4=  ""
        else:
            query4=  " BOOKS.isbn like concat('%', '" + search_isbn + "', '%')"
        
        query5 = " group by BOOKS.isbn,BOOKS.title;"

        if(search_isbn=='' and search_author=='' and search_title==''):
            query_final = "select BOOKS.isbn, BOOKS.title, AUTHORS.name from BOOKS join BOOK_AUTHORS on BOOKS.isbn = BOOK_AUTHORS.isbn join AUTHORS on BOOK_AUTHORS.author_id = AUTHORS.author_id where BOOKS.title like concat('%', ' ', '%') or AUTHORS.name like concat('%', ' ', '%') or BOOKS.isbn like concat('%', ' ', '%') group by BOOKS.isbn,BOOKS.title;"
        else:
            if(query2=='' and (query3!='' and query4!='')):
                query_final = query1+query3+"and"+query4+query5
            elif(query3=='' and (query2!='' and query4!='')):
                query_final = query1+query2+"and"+query4+query5
            elif(query4=='' and (query3!='' and query2!='')):
                query_final = query1+query2+"and"+query3+query5
            elif(query2!='' and (query3=='' and query4=='')):
                query_final = query1+query2+query5
            elif(query3!='' and (query2=='' and query4=='')):
                query_final = query1+query3+query5
            elif(query4!='' and (query3=='' and query2=='')):
                query_final = query1+query4+query5
            elif(query3!='' and query2!='' and query3!=''):
                query_final=query1+query2+query3+query4+query5
        cursor = cnx.cursor()
        cursor.execute(query_final)

        self.data = cursor.fetchall()
        self.view_data()

    def view_data(self):
        self.ResultTreeview.delete(*self.ResultTreeview.get_children())
        for elem in self.data:
            cursor = cnx.cursor()
            cursor.execute("SELECT EXISTS(SELECT BOOK_LOANS.isbn from BOOK_LOANS where BOOK_LOANS.isbn = '" + str(elem[0]) + "')")
            result = cursor.fetchall()
            if result == [(0,)]:
                availability = "Available"
                doa = todays_date.date()
            else:
                cursor = cnx.cursor()
                cursor.execute("SELECT BOOK_LOANS.Date_in, BOOK_LOANS.due_date from BOOK_LOANS where BOOK_LOANS.isbn = '" + str(elem[0]) + "'")
                output = cursor.fetchall()
                print(output[-1][0])
                if output[-1][0] is None:
                    availability = "Not Available"
                    doa = output[0][1]
                else:
                    availability = "Available"
                    doa = todays_date.date()
            
            cnx.commit()
            self.ResultTreeview.insert('', 'end', text=str(elem[0]),
                                       values=(elem[1], elem[2], availability, doa))

    def selectBookForCheckout(self, a):
        curItem = self.ResultTreeview.focus()
        self.bookForCheckOutIsbn = self.ResultTreeview.item(curItem)['text']

    def check_out(self):
        if self.bookForCheckOutIsbn is None:
            messagebox.showinfo("Attention!", "Select Book First!")
            return None
        self.borrowerId = simpledialog.askstring("Check Out Book", "Enter Borrower ID")
        cursor = cnx.cursor()
        cursor.execute("SELECT EXISTS(SELECT Card_id from BORROWER WHERE BORROWER.Card_id = '" + str(self.borrowerId) + "')")
        result = cursor.fetchall()

        if result == [(0,)]:
            messagebox.showinfo("Error", "Borrower not in Database!")
            return None
        else:
            count = 0
            cursor = cnx.cursor()
            cursor.execute("SELECT BOOK_LOANS.Date_in from BOOK_LOANS WHERE BOOK_LOANS.Card_id = '" + str(self.borrowerId) + "'")
            result = cursor.fetchall()
            for elem in result:
                if elem[0] is None:
                    count += 1
            if count >= 3:
                messagebox.showinfo("Not Allowed!", "Borrower has loaned 3 books already!")
                return None
            
            else:
                cursor.execute("SELECT COUNT(*) FROM BOOK_LOANS WHERE Isbn= '" + self.bookForCheckOutIsbn + "' and date_in is null")
                cnt = cursor.fetchall()
                if cnt == [(1,)]:
                    messagebox.showinfo("Attention!", "Book has already loaned out!")
                    return None
                else:
                    cursor = cnx.cursor()
                    cursor.execute("SET FOREIGN_KEY_CHECKS=0")
                    cursor.execute("INSERT INTO BOOK_LOANS (ISBN, Card_id, Date_out, Due_date) VALUES ('" + self.bookForCheckOutIsbn + "', '" + self.borrowerId + "', '" + str(todays_date) + "', '" + str(todays_date + timedelta(days=14)) + "')")
                    cursor.execute("SET FOREIGN_KEY_CHECKS=1")
                    cnx.commit()
                    cursor = cnx.cursor()
                    cursor.execute("SELECT MAX(Loan_Id) FROM BOOK_LOANS")
                    result = cursor.fetchall()
                    loan_id = result[0][0]
                    cursor.execute("INSERT INTO FINES (Loan_Id, fine_amt, paid) VALUES ('" + str(loan_id) + "', '0.00', '0')")
                    cnx.commit()
                    messagebox.showinfo("Done", "Book Loaned Out!")

    def check_in(self):
        self.checkInWindow = Toplevel(self.parent)
        self.checkInWindow.title("Check In Here")
        self.app = CheckIn(self.checkInWindow)
        #self.ResultTreeview.delete(*self.ResultTreeview.get_children())

    def update_fines(self):
        cursor = cnx.cursor()
        cursor.execute("SELECT BOOK_LOANS.Loan_Id, BOOK_LOANS.Date_in, BOOK_LOANS.Due_date FROM BOOK_LOANS")
        result = cursor.fetchall()
        for record in result:
            date_in = record[1]
            date_due = record[2]
            if date_in is None:
                date_in = todays_date.date()
            diff = date_in - date_due
            if diff.days > 0:
                fine = int(diff.days) * 0.25
            else:
                fine = 0
            
            cursor = cnx.cursor()
            cursor.execute("UPDATE FINES SET FINES.fine_amt = '" + str(fine) + "' WHERE FINES.Loan_Id = '" + str(record[0]) + "'")
            cnx.commit()
        messagebox.showinfo("Info", "Generated Fines")

    def pay_fines(self):
        self.newPayFinesWindow = Toplevel(self.parent)
        self.newPayFinesWindow.title("Fine!!")
        self.app1 = PayFines(self.newPayFinesWindow)

    def add_borrower(self):
        self.newBorrowerWindow = Toplevel(self.parent)
        self.newBorrowerWindow.title("Adding New Borrower")
        self.newapp = Borrower(self.newBorrowerWindow)