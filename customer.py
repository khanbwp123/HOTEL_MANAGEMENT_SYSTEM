from tkinter import*
from PIL import Image, ImageTk
from tkinter import ttk
import random
import mysql.connector
from tkinter import messagebox


class Cust_Win:
     def __init__(self,root):
         self.root=root
         self.root.title("Hotel Management System")
         self.root.geometry("1295x550+230+220")
         self.root.minsize(800, 500)
         self.root.resizable(True, True)

         #=====random variable===
         # =====random variable===
         self.var_Ref = StringVar()
         x = random.randint(1000, 9999)
         self.var_Ref.set(str(x))

         self.var_cust_name = StringVar()
         self.var_mother = StringVar()
         self.var_gender = StringVar()
         self.var_post = StringVar()
         self.var_mobile = StringVar()
         self.var_email = StringVar()
         self.var_nationality = StringVar()
         self.var_address = StringVar()
         self.var_id_proof = StringVar()
         self.var_id_number = StringVar()





         # =======title========
         lbl_title = Label(self.root, text="ADD CUSTOMER DETAILS",font=("times new roman", 18, "bold"),bg="black", fg="gold", bd=4, relief=RIDGE)
         lbl_title.place(x=0,y=0, width=1295,height=50)

         #======LOGO==========
         img2 = Image.open(r"C:\Users\SAEEDCOMPUTERS\Downloads\img2.png")
         img2 = img2.resize((100, 40), Image.Resampling.LANCZOS)
         self.photoimg2 = ImageTk.PhotoImage(img2)

         lblimg = Label(self.root, image=self.photoimg2, bd=0, relief=RIDGE)
         lblimg.place(x=5, y=2, width=100, height=40)


         #========LABELFRAME======
         labelframeleft=LabelFrame(self.root,bd=2,relief=RIDGE,text="Customer Details",font=("arial", 12, "bold"),padx=2)
         labelframeleft.place(x=5, y=50, width=425, height=530)  # was 490

         # Customer Reference (row 0)
         lbl_cust_ref = Label(labelframeleft, text="Customer Ref", font=("arial", 12, "bold"), padx=2, pady=6)
         lbl_cust_ref.grid(row=0, column=0, sticky=W)

         enty_ref = ttk.Entry(labelframeleft,textvariable=self.var_Ref, width=29, font=("arial", 13, "bold"),state="readonly")
         enty_ref.grid(row=0, column=1)

         # Customer Name (row 1)
         cname = Label(labelframeleft, text="Customer name", font=("arial", 12, "bold"), padx=2, pady=6)
         cname.grid(row=1, column=0, sticky=W)

         txtcname = ttk.Entry(labelframeleft,textvariable=self.var_cust_name, width=29, font=("arial", 13, "bold"))
         txtcname.grid(row=1, column=1)

         #======mother name=====
         lblmname = Label(labelframeleft, text="Mother name", font=("arial", 12, "bold"), padx=2, pady=6)
         lblmname.grid(row=2, column=0, sticky=W)

         txtmname= ttk.Entry(labelframeleft,textvariable=self.var_mother, width=29, font=("arial", 13, "bold"))
         txtmname.grid(row=2, column=1)

         #gender comobox=====
         label_gender=Label(labelframeleft,font=("arial",12,"bold"),text="Gender",padx=2,pady=6)
         label_gender.grid(row=3,column=0,sticky=W)

         combo_gender=ttk.Combobox(labelframeleft,textvariable=self.var_gender,font=("arial", 12, "bold"),width=27,state="readonly")
         combo_gender["value"]=("Male","Female","Others")
         combo_gender.current(0)
         combo_gender.grid(row=3,column=1)




         #postcode
         lblPostCode= Label(labelframeleft, text="Post Code", font=("arial", 12, "bold"), padx=2, pady=6)
         lblPostCode.grid(row=4, column=0, sticky=W)
         txtPostCode = ttk.Entry(labelframeleft, textvariable=self.var_post, width=29, font=("arial", 13, "bold"))
         txtPostCode.grid(row=4, column=1)

         #mobile numbr
         lblMobile = Label(labelframeleft, text="Mobile", font=("arial", 12, "bold"), padx=2, pady=6)
         lblMobile.grid(row=5, column=0, sticky=W)
         txtMobile = ttk.Entry(labelframeleft,textvariable=self.var_mobile, width=29, font=("arial", 13, "bold"))
         txtMobile.grid(row=5, column=1)

         #email
         lblEmail = Label(labelframeleft, text="Email", font=("arial", 12, "bold"), padx=2, pady=6)
         lblEmail.grid(row=6, column=0, sticky=W)
         txtEmail = ttk.Entry(labelframeleft,textvariable=self.var_email, width=29, font=("arial", 13, "bold"))
         txtEmail.grid(row=6, column=1)

         #nationality
         lblNationality= Label(labelframeleft,text="Nationality",font=("arial", 12, "bold"), padx=2, pady=6)
         lblNationality.grid(row=7, column=0, sticky=W)

         combo_Nationality = ttk.Combobox(labelframeleft,textvariable=self.var_nationality,font=("arial", 12, "bold"), width=27, state="readonly")
         combo_Nationality["value"] = ("PAKISTANI", "AMERICAN", "CANADIAN")
         combo_Nationality.current(0)
         combo_Nationality.grid(row=7, column=1)


         #id proof combobox
         lblIdProof=Label(labelframeleft,font=("arial", 12, "bold"), padx=2, pady=6,text="Id Proof Type")
         lblIdProof.grid(row=8, column=0, sticky=W)


         combo_id = ttk.Combobox(labelframeleft,textvariable=self.var_id_proof, font=("arial", 12, "bold"), width=27, state="readonly")
         combo_id["value"] = ("ID CARD", "DRIVING LICENCE", "PASSPORT NUMBER")
         combo_id.current(0)
         combo_id.grid(row=8, column=1)

         #ID NUMBER
         lblIdNumber = Label(labelframeleft, font=("arial", 12, "bold"), padx=2, pady=6, text="ID NUMBER")
         lblIdNumber.grid(row=9, column=0, sticky=W)
         txtIdNumber= ttk.Entry(labelframeleft,textvariable=self.var_id_number, width=29, font=("arial", 13, "bold"))
         txtIdNumber.grid(row=9, column=1)


         #address
         lblAddress = Label(labelframeleft, font=("arial", 12, "bold"), padx=2, pady=6, text = "ADDRESS")
         lblAddress.grid(row=10, column=0, sticky=W)
         txtAddress = ttk.Entry(labelframeleft,textvariable=self.var_address, width=29, font=("arial", 13, "bold"))
         txtAddress.grid(row=10, column=1)
         #BUTTON frame
         btn_frame=Frame(labelframeleft,bd=2,relief=RIDGE)
         btn_frame.place(x=0,y=400,width=412,height=40)

         btn_Add=Button(btn_frame,text="Add",command=self.add_data,font=("arial", 12, "bold"),bg="black",fg="gold",width=10)
         btn_Add.grid(row=0,column=0,padx=1)

         btn_Update = Button(btn_frame, text="UPDATE",command=self.update,font=("arial", 12, "bold"), bg="black", fg="gold", width=10)
         btn_Update.grid(row=0, column=1, padx=1)

         btn_Delete = Button(btn_frame,text="DELETE",command=self.mDelete,font=("arial", 12, "bold"), bg="black", fg="gold", width=10)
         btn_Delete.grid(row=0, column=2, padx=1)

         btn_Reset= Button(btn_frame, text="RESET",command=self.reset,font=("arial", 12, "bold"), bg="black", fg="gold", width=8)
         btn_Reset.grid(row=0, column=3, padx=1)

         #table frame search sys
         Table_Frame= LabelFrame(self.root, bd=2, relief=RIDGE, text="VIEW DETAILS AND SEARCH SYSTEM", font=("arial", 12, "bold"),padx=2)
         Table_Frame.place(x=435, y=50, width=860, height=490)  # was 490

         lblSearchBy = Label(Table_Frame, font=("arial", 12, "bold"),text="SEARCH BY",bg="red",fg="white")
         lblSearchBy.grid(row=0, column=0, sticky=W,padx=2)


         self.search_var=StringVar()
         combo_Search = ttk.Combobox(Table_Frame,textvariable=self.search_var, font=("arial", 12, "bold"), width=24, state="readonly")
         combo_Search["value"] = ("Mobile No.", "Ref No.")
         combo_Search.grid(row=0, column=1,padx=2)

         self.txt_search=StringVar()
         txtSearch= ttk.Entry(Table_Frame,textvariable=self.txt_search, width=24,font=("arial", 13, "bold"))
         txtSearch.grid(row=0, column=2,padx=2)

         btn_Search = Button(Table_Frame, text="SEARCH",command=self.search, font=("arial", 12, "bold"), bg="black", fg="gold", width=10)
         btn_Search.grid(row=0, column=3, padx=1)

         btn_ShowAll = Button(Table_Frame, text="Show All",command=self.fetch_data, font=("arial", 12, "bold"), bg="black", fg="gold", width=10)
         btn_ShowAll.grid(row=0, column=4, padx=1)

         #=======SHOW DATA TABLE=====

         details_table = Frame(Table_Frame, bd=2, relief=RIDGE)
         details_table.place(x=0, y=50, width=860, height=350)

         scroll_x=ttk.Scrollbar(details_table,orient=HORIZONTAL)
         scroll_y=ttk.Scrollbar(details_table,orient=VERTICAL)

         self.Cust_Details_Table=ttk.Treeview(details_table,column=("Ref","Name","Mother","Gender","Post","Mobile","Email"
                                              ,"Nationality","ID Proof","ID No.","Address"),xscrollcommand=scroll_x.set
                                              ,yscrollcommand=scroll_y.set)

         scroll_x.pack(side=BOTTOM,fill=X)
         scroll_y.pack(side=LEFT,fill=Y)

         scroll_x.config(command=self.Cust_Details_Table.xview)
         scroll_y.config(command=self.Cust_Details_Table.yview)

         self.Cust_Details_Table.heading("Ref",text="Refer No.")
         self.Cust_Details_Table.heading("Name", text="Name")
         self.Cust_Details_Table.heading("Mother",text="Mother")
         self.Cust_Details_Table.heading("Gender",text="Gender")
         self.Cust_Details_Table.heading("Post",text="Post")
         self.Cust_Details_Table.heading("Mobile",text="Mobile")
         self.Cust_Details_Table.heading("Email",text="Email")
         self.Cust_Details_Table.heading("Nationality",text="Nationality")
         self.Cust_Details_Table.heading("ID Proof",text="ID Proof")
         self.Cust_Details_Table.heading("ID No.",text="ID No.")
         self.Cust_Details_Table.heading("Address",text="Address")

         self.Cust_Details_Table["show"]="headings"

         self.Cust_Details_Table.column("Ref",width=100)
         self.Cust_Details_Table.column("Name", width=100)
         self.Cust_Details_Table.column("Mother", width=100)
         self.Cust_Details_Table.column("Gender", width=100)
         self.Cust_Details_Table.column("Post", width=100)
         self.Cust_Details_Table.column("Mobile", width=100)
         self.Cust_Details_Table.column("Email", width=100)
         self.Cust_Details_Table.column("Nationality", width=100)
         self.Cust_Details_Table.column("ID Proof", width=100)
         self.Cust_Details_Table.column("ID No.", width=100)
         self.Cust_Details_Table.column("Address", width=100)




         self.Cust_Details_Table.pack(fill=BOTH,expand=1)
         self.Cust_Details_Table.bind("<ButtonRelease-1>",self.get_cursor)
         self.fetch_data()

     def add_data(self):
         if self.var_mobile.get() == "" or self.var_mother.get() == "":
             messagebox.showerror("ERROR", "All fields are required")
         else:
             try:
                 conn = mysql.connector.connect(host="localhost", username="root", password="11223344",
                                                database="hotel")
                 my_cursor = conn.cursor()
                 my_cursor.execute(
                     "INSERT INTO customer (Ref, Name, Mother, Gender, Post, Mobile, Email, Nationality, ID_Proof, ID_No, Address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                     (
                         self.var_Ref.get(),
                         self.var_cust_name.get(),
                         self.var_mother.get(),
                         self.var_gender.get(),
                         self.var_post.get(),
                         self.var_mobile.get(),
                         self.var_email.get(),
                         self.var_nationality.get(),
                         self.var_id_proof.get(),
                         self.var_id_number.get(),
                         self.var_address.get()
                     )
                 )

                 conn.commit()
                 self.fetch_data()
                 conn.close()
                 messagebox.showinfo("Success", "customer has been added", parent=self.root)
             except Exception as es:
                 messagebox.showwarning("Warning", f"Something went wrong:{str(es)}", parent=self.root)

     # ... (rest of your Cust_Win class methods) ...

     def fetch_data(self):
         conn=mysql.connector.connect(host="localhost", username="root", password="11223344",database="hotel")
         my_cursor = conn.cursor()
         my_cursor.execute("select * from customer")
         rows=my_cursor.fetchall()
         if len(rows)!=0:
             self.Cust_Details_Table.delete(*self.Cust_Details_Table.get_children())
             for i in rows:
                 self.Cust_Details_Table.insert("",END,values=i)
             conn.commit()
         conn.close()
     def get_cursor(self,event=""):
        cursor_row=self.Cust_Details_Table.focus()
        content=self.Cust_Details_Table.item(cursor_row)
        row=content["values"]

        self.var_Ref.set(row[0]),
        self.var_cust_name.set(row[1]),
        self.var_mother.set(row[2]),
        self.var_gender.set(row[3]),
        self.var_post.set(row[4]),
        self.var_mobile.set(row[5]),
        self.var_email.set(row[6]),
        self.var_nationality.set(row[7]),
        self.var_id_proof.set(row[8]),
        self.var_id_number.set(row[9]),
        self.var_address.set(row[10])


     def update(self):
        if self.var_mobile.get()=="":
            messagebox.showerror("Error","Please enter mobile number",parent=self.root)
        else:
            conn = mysql.connector.connect(host="localhost", username="root", password="11223344",database="hotel")
            my_cursor=conn.cursor()
            my_cursor.execute("update customer set Name=%s,Mother=%s,Gender=%s,Post=%s,Mobile=%s,Email=%s,Nationality=%s,ID_Proof=%s,ID_No=%s,Address=%s where Ref=%s",(

                                                                                                                                                        self.var_cust_name.get(),
                                                                                                                                                        self.var_mother.get(),
                                                                                                                                                        self.var_gender.get(),
                                                                                                                                                        self.var_post.get(),
                                                                                                                                                        self.var_mobile.get(),
                                                                                                                                                        self.var_email.get(),
                                                                                                                                                        self.var_nationality.get(),
                                                                                                                                                        self.var_id_proof.get(),
                                                                                                                                                        self.var_id_number.get(),
                                                                                                                                                        self.var_address.get(),
                                                                                                                                                        self.var_Ref.get()))
            conn.commit()
            self.fetch_data()
            conn.close()
            messagebox.showinfo("Update","Customer details are updated successfully",parent=self.root)


     def mDelete(self):
        mDelete=messagebox.askyesno("Hotel Management System","Do you want to delete this customer",parent=self.root)
        if mDelete>0:
            conn = mysql.connector.connect(host="localhost", username="root", password="11223344", database="hotel")
            my_cursor = conn.cursor()
            query="delete from customer where ref=%s"
            value=(self.var_Ref.get(),)
            my_cursor.execute(query,value)
        else:
            if not mDelete:
                return
        conn.commit()
        self.fetch_data()
        conn.close()

     def reset(self):
         #self.var_Ref.set("")
         self.var_cust_name.set(""),
         self.var_mother.set(""),
         #self.var_gender.set(""),
         self.var_post.set(""),
         self.var_mobile.set(""),
         self.var_email.set(""),
         #self.var_nationality.set(""),
         #self.var_id_proof.set(""),
         self.var_id_number.set(""),
         self.var_address.set("")


         x = random.randint(1000, 9999)
         self.var_Ref.set(str(x))

     def search(self):
         conn = mysql.connector.connect(host="localhost", username="root", password="11223344", database="hotel")
         my_cursor = conn.cursor()

         # Map display names to actual column names in the database
         search_by = self.search_var.get()
         if search_by == "Mobile No.":
             column_name = "Mobile"
         elif search_by == "Ref No.":
             column_name = "Ref"
         else:
             messagebox.showerror("Error", "Invalid search criteria", parent=self.root)
             return

         query = f"SELECT * FROM customer WHERE {column_name} LIKE %s"
         value = ("%" + self.txt_search.get() + "%",)
         my_cursor.execute(query, value)

         rows = my_cursor.fetchall()
         if rows:
             self.Cust_Details_Table.delete(*self.Cust_Details_Table.get_children())
             for row in rows:
                 self.Cust_Details_Table.insert("", END, values=row)
         else:
             messagebox.showinfo("Not Found", "No matching records found", parent=self.root)

         conn.close()
if __name__ == '__main__':
    root=Tk()
    obj=Cust_Win(root)
    root.mainloop()


