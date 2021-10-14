from tkinter import *
import tkinter.messagebox
import sqlite3
import Database

#Frontend

class Login:
    def __init__(self, master):
        self.master = master
        self.master.title("Pharmacy Management System")
        self.master.geometry('1350x750+0+0')
        self.master.config(bg='midnight blue')
        self.frame = Frame(self.master, bg='midnight blue')
        self.frame.pack()

        self.Username = StringVar()
        self.Password = StringVar()

        self.lblTitle = Label(self.frame, text='LOGIN', font=('Chalkduster', 70, 'bold'), bg='midnight blue',
                              fg='gold')
        self.lblTitle.grid(row=0, column=0, columnspan=2, pady=40)
        # =============================================================================================
        self.LoginFrame1 = LabelFrame(self.frame, width=1350, height=600,bg='midnight blue', bd=5)
        self.LoginFrame1.grid(row=1, column=0,pady=2)

        self.LoginFrame2 = LabelFrame(self.frame, width=1350, height=600, bg='midnight blue', bd=5)
        self.LoginFrame2.grid(row=2, column=0,pady=15)

        # ===========================================Label and Entry====================================

        self.lblUsername = Label(self.LoginFrame1, text='Net ID', font=('Times New Roman', 25, 'bold'),
                                 bg='midnight blue', fg='gold')
        self.lblUsername.grid(row=0, column=0)

        self.txtUsername = Entry(self.LoginFrame1, font=('arial', 20, 'bold'), bd=7, textvariable=self.Username,
                                 width=30,bg='white smoke')
        self.txtUsername.grid(row=0, column=1, padx=10,pady=10)

        self.lblPassword = Label(self.LoginFrame1, text='Password', font=('Times New Roman', 25, 'bold'),
                                 bg='midnight blue', fg='gold')
        self.lblPassword.grid(row=1, column=0)

        self.txtPassword = Entry(self.LoginFrame1, font=('arial', 20, 'bold'), show='*', bd=7,
                                 textvariable=self.Password,
                                 width=30,bg='white smoke')
        self.txtPassword.grid(row=1, column=1, columnspan=2, pady=30)

        # ===========================================Buttons============================================
        self.btnLogin = Button(self.LoginFrame2, text='LOGIN', width=17, font=('arial', 20, 'bold'),command=self.Login_System)
        self.btnLogin.grid(row=3, column=0, pady=20, padx=8)

        self.btnReset = Button(self.LoginFrame2, text='RESET', width=17, font=('arial', 20, 'bold'),command=self.Reset)
        self.btnReset.grid(row=3, column=1, pady=20, padx=8)

        self.btnExit = Button(self.LoginFrame2, text='EXIT', width=17, font=('arial', 20, 'bold'),command=self.iExit)
        self.btnExit.grid(row=3, column=2, pady=20, padx=8)
        # ===========================================Buttons============================================

    def Login_System(self):
        global username, password
        username = (self.Username.get())
        password = (self.Password.get())
        login= Database.authenticate_login(username, password)
        if login:
            self.new_window()
        else:
            tkinter.messagebox.askyesno("Login System", "Invalid login detail")
            self.Username.set("")
            self.Password.set("")
            self.txtUsername.focus()

    def Reset(self):
        self.Username.set("")
        self.Password.set("")
        self.txtUsername.focus()

    def iExit(self):
        self.iExit = tkinter.messagebox.askyesno("Pharmacy Management Login System", "Confirm if you want to exit")
        if self.iExit > 0:
            self.master.destroy()
        else:
            # command = self.new_window
            return

    def new_window(self):
        self.newWindow = Toplevel(self.master)
        self.app = Medicines(self.newWindow, self.master)


class Medicines:

    def __init__(self,root, root2):
        self.root2= root2
        self.root = root
        self.root.title("Pharmacy Management System")
        self.root.geometry("1350x750+0+0")
        self.root.config(bg="midnight blue")

        self.frame1 = Frame(self.root, bg='midnight blue')
        self.frame1.pack()

        # Initialise the cells of the GUI window to be StringVar
        MedicineName = StringVar()
        Price = StringVar()

         #=========================================Function Declaration================================================

        def addData():
            if(len(MedicineName.get())!=0):
                DisplayData3()
                cartList.insert(END, sd)

        # The databses as well as the ListBox contents are updated in these functions i.e based on buttom click update database as well as the ListBox
        def Delete():
            cartList.delete(searchCart)
            Display_after_delete()

        def searchDatabase():
            medicineList.delete(0, END)
            for row in Database.searchData(MedicineName.get()):
                medicineList.insert(END,row[1])

        def DisplayData():
            medicineList.delete(0,END)
            for row in Database.viewData():
                qty= len([x for x in cartList.get(0, END) if x in row[1]])
                # -1 because I am reading the medicines that are there in the cart but also have to account for the current
                # selection, which is about to be added. Which means I am evaluating the Quantity that would be
                # available for each medicine should it be added to the cart
                if (Database.get_quantity(row[1]) - qty) > 0:
                        medicineList.insert(END, row[1])
                else:
                    Database.outofstock_meds(row[0], row[1])


        def DisplayData3():
            medicineList.delete(0,END)
            for row in Database.viewData():
                qty= len([x for x in cartList.get(0, END) if x in row[1]])
                if row[1]==sd:
                    if (Database.get_quantity(row[1]) - qty - 1) > 0:
                        medicineList.insert(END, row[1])
                    else:
                        Database.outofstock_meds(row[0], row[1])
                else:
                    if (Database.get_quantity(row[1]) - qty) > 0:
                        medicineList.insert(END, row[1])
                    else:
                        Database.outofstock_meds(row[0], row[1])

        def Display_after_delete():
            medicineList.delete(0,END)
            for row in Database.viewData():
                qty= len([x for x in cartList.get(0, END) if x in row[1]])
                if (Database.get_quantity(row[1]) - qty) > 0:
                    medicineList.insert(END, row[1])

                    # In case after a delete operation, any medicine previously inserted
                    # to outofstock_meds becomes avaliable again, remove it from outofstock_meds table
                    con = sqlite3.connect("pharmacy.db")
                    cur = con.cursor()
                    cur.execute("DELETE FROM outofstock_meds WHERE id= ?", (row[0],))
                    con.commit()
                    con.close()

        def BuyMeds():
            rows = cartList.get(0, END)
            Database.transact(rows, username, root2)

        def MedicineRec(event):
            global sd

            searchStd = medicineList.curselection()[0] # medicineList.curselection()[0] returns the index of the item selected from the ListBox
            sd = medicineList.get(searchStd) # it stores the entire selected record

            # Delete whats there in the Search Medicine Name Entry Frame and then insert the name from the selected record
            self.txtMedicineName.delete(0,END)
            self.txtMedicineName.insert(END,sd)

            price= Database.get_price(sd)
            self.txtMedicinePrice.delete(0, END)
            self.txtMedicinePrice.insert(END, "Rs. " + str(price))

        def CartRec(event2):
            global ct, searchCart

            searchCart = cartList.curselection()[0]
            ct = cartList.get(searchCart)

            self.txtMedicineName.delete(0, END)
            self.txtMedicineName.insert(END, ct)

            price = Database.get_price(ct)
            self.txtMedicinePrice.delete(0, END)
            self.txtMedicinePrice.insert(END, "Rs. " + str(price))


        #=========================================Frame================================================================
        MainFrame = Frame(self.root, bg="midnight blue")
        MainFrame.pack()

        self.titframe = Label(self.frame1, text='Hello Student!', font=('Chalkduster', 50, 'bold'), bg='midnight blue',fg='gold')
        self.titframe.grid(row=0, column=0, pady=20, padx=10)

        ButtonFrame =Frame(MainFrame,bd=2, width=1350, height=500, padx=18,pady=10, bg="midnight blue")
        ButtonFrame.pack(side=TOP)

        DataFrame =Frame(MainFrame, bd=2, width=1350, height=500, padx=18, pady=10,bg="midnight blue")
        DataFrame.pack(side=BOTTOM)

        DataFrameBOTTOM =LabelFrame(DataFrame, bd=2, width=1000, height=600, padx=0, font=('arial', 20,'bold'), bg="midnight blue")
        DataFrameBOTTOM.pack(side=BOTTOM)
        
        DataFrameLEFT = LabelFrame(DataFrame, bd=2, width=450, height=300, padx=31,pady=3,font=('arial', 20,'bold'),bg="Ghost White", text="MEDICINES:")
        DataFrameLEFT.pack(side=LEFT)

        DataFrameRIGHT = LabelFrame(DataFrame, bd=2, width=450, height=300, padx=31, pady=3,font=('arial', 20, 'bold'), bg="Ghost White", text="CART:")
        DataFrameRIGHT.pack(side=RIGHT)

        #=========================================Labels and Entrys===============================================
        self.lblMedicineName = Label(ButtonFrame,font=('Chalkduster',25,'bold'),text="SEARCH: ",bg="midnight blue",fg='gold')
        self.lblMedicineName.grid(row=0,column =0,sticky=W)
        self.txtMedicineName = Entry(ButtonFrame,font=('Times New Roman',20,'bold'), textvariable=MedicineName, width=45,bg='ghost white')
        self.txtMedicineName.grid(row=0,column=1,pady=5)

        self.lblMedicinePrice = Label(ButtonFrame, font=('Chalkduster', 25, 'bold'), text="PRICE: ", bg="midnight blue",fg='gold')
        self.lblMedicinePrice.grid(row=1, column=0, sticky=W)
        self.txtMedicinePrice = Entry(ButtonFrame,font=('Times New Roman',20,'bold'), textvariable=Price, width=45,bg='ghost white')
        self.txtMedicinePrice.grid(row=1,column=1,pady=2)

        # Best way to understand this section is to go through ListBox and Scrollbar from Tkinter's documentation
        #=========================================Listbox and Scrollbar===============================================

        scrollbar = Scrollbar(DataFrameLEFT)
        scrollbar.grid(row=4, column=1, sticky ='ns')
        medicineList = Listbox(DataFrameLEFT, width = 41, height=16, font=('arial', 15,'bold'), yscrollcommand=scrollbar.set)
        medicineList.bind('<<ListboxSelect>>', MedicineRec)
        medicineList.grid(row=4, column=0, padx=16)
        scrollbar.config(command=medicineList.yview)

        scrollbar2 = Scrollbar(DataFrameRIGHT)
        scrollbar2.grid(row=4, column=1, sticky='ns')
        cartList = Listbox(DataFrameRIGHT, width=41, height=16, font=('arial', 15, 'bold'), yscrollcommand=scrollbar2.set)
        cartList.bind('<<ListboxSelect>>', CartRec)
        cartList.grid(row=4, column=0, padx=16)
        scrollbar2.config(command=cartList.yview)

        DisplayData()

        #=========================================Buttons Widget=====================================================
        self.btnAddData=Button(DataFrameLEFT, text='ADD', font=('arial', 20,'bold'),height=1, width=10, bd=4, command=addData)
        self.btnAddData.grid(row=5,column=0)

        self.btnDeleteData=Button(DataFrameRIGHT, text='DELETE', font=('arial', 20,'bold'),height=1, width=10, bd=4, command=Delete)
        self.btnDeleteData.grid(row=5,column=0)

        self.btnSearchData = Button(ButtonFrame, text='Search', font=('arial', 20, 'bold'), height=1, width=10, bd=4, command=searchDatabase)
        self.btnSearchData.grid(row=0,column=3,padx=5)

        self.btnDisplayData=Button(ButtonFrame, text='Display All', font=('arial', 20,'bold'),height=1, width=12,bd=4, command=DisplayData)
        self.btnDisplayData.grid(row=0,column=4,padx=3)

        self.btnBuy=Button(DataFrameBOTTOM, text='BUY', font=('arial', 20, 'bold'), height=1, width=10, bd=4, command=BuyMeds)
        self.btnBuy.pack(side=BOTTOM)


if __name__=='__main__':
    global root
    root = Tk()
    application = Login(root)
    root.mainloop()
