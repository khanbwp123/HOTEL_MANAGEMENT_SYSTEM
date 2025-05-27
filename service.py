# service.py
from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
import random # For generating simple service IDs

class Service_Win:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System - Service Details")
        self.root.geometry("900x500+230+220") # Adjusted geometry for services
        self.root.minsize(600, 400)
        self.root.resizable(True, True)

        # ======= Variables =======
        self.var_service_id = StringVar()
        x = random.randint(100, 999) # Generate a 3-digit ID
        self.var_service_id.set(str(x))

        self.var_service_name = StringVar()
        self.var_service_price = StringVar()


        # ======= Title =======
        lbl_title = Label(self.root, text="HOTEL SERVICES MANAGEMENT", font=("times new roman", 18, "bold"),
                          bg="black", fg="gold", bd=4, relief=RIDGE)
        lbl_title.place(x=0, y=0, width=900, height=50)

        # ======= Left Frame (Form) =======
        labelframeleft = LabelFrame(self.root, bd=2, relief=RIDGE, text="Add/Update Service",
                                    font=("arial", 12, "bold"), padx=2)
        labelframeleft.place(x=5, y=50, width=400, height=250)

        # Service ID
        lbl_service_id = Label(labelframeleft, text="Service ID:", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_service_id.grid(row=0, column=0, sticky=W)
        enty_service_id = ttk.Entry(labelframeleft, textvariable=self.var_service_id, width=20,
                                    font=("arial", 13, "bold"), state="readonly")
        enty_service_id.grid(row=0, column=1, sticky=W)

        # Service Name
        lbl_service_name = Label(labelframeleft, text="Service Name:", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_service_name.grid(row=1, column=0, sticky=W)
        enty_service_name = ttk.Entry(labelframeleft, textvariable=self.var_service_name, width=20,
                                      font=("arial", 13, "bold"))
        enty_service_name.grid(row=1, column=1, sticky=W)

        # Service Price
        lbl_service_price = Label(labelframeleft, text="Price (Rs.):", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_service_price.grid(row=2, column=0, sticky=W)
        enty_service_price = ttk.Entry(labelframeleft, textvariable=self.var_service_price, width=20,
                                       font=("arial", 13, "bold"))
        enty_service_price.grid(row=2, column=1, sticky=W)

        # ======= Button Frame =======
        btn_frame = Frame(labelframeleft, bd=2, relief=RIDGE)
        btn_frame.place(x=0, y=180, width=390, height=40)

        Button(btn_frame, text="Add", command=self.add_data, font=("arial", 11, "bold"),
               bg="black", fg="gold", width=9).grid(row=0, column=0, padx=1)
        Button(btn_frame, text="UPDATE", command=self.update, font=("arial", 11, "bold"),
               bg="black", fg="gold", width=9).grid(row=0, column=1, padx=1)
        Button(btn_frame, text="DELETE", command=self.mDelete, font=("arial", 11, "bold"),
               bg="black", fg="gold", width=9).grid(row=0, column=2, padx=1)
        Button(btn_frame, text="RESET", command=self.reset_data, font=("arial", 11, "bold"),
               bg="black", fg="gold", width=8).grid(row=0, column=3, padx=1)

        # ======= Table Frame (Display Services) =======
        Table_Frame = LabelFrame(self.root, bd=2, relief=RIDGE, text="View Hotel Services",
                                 font=("arial", 12, "bold"), padx=2)
        Table_Frame.place(x=410, y=55, width=480, height=400)

        scroll_x = ttk.Scrollbar(Table_Frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(Table_Frame, orient=VERTICAL)

        self.service_table = ttk.Treeview(Table_Frame,
                                          columns=("service_id", "service_name", "service_price"),
                                          xscrollcommand=scroll_x.set,
                                          yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.service_table.xview)
        scroll_y.config(command=self.service_table.yview)

        self.service_table.heading("service_id", text="ID")
        self.service_table.heading("service_name", text="Service Name")
        self.service_table.heading("service_price", text="Price (Rs.)")

        self.service_table["show"] = "headings"
        self.service_table.column("service_id", width=50)
        self.service_table.column("service_name", width=150)
        self.service_table.column("service_price", width=100)

        self.service_table.pack(fill=BOTH, expand=1)

        self.service_table.bind("<ButtonRelease-1>", self.get_cursor)
        self.fetch_data() # Load existing service data on startup

    # ========== CRUD Operations ==========

    def add_data(self):
        if self.var_service_name.get() == "" or self.var_service_price.get() == "":
            messagebox.showerror("ERROR", "Service Name and Price are required!", parent=self.root)
        else:
            try:
                # Validate price is a number
                float(self.var_service_price.get())

                conn = mysql.connector.connect(host="localhost", username="root", password="11223344", database="hotel")
                my_cursor = conn.cursor()
                my_cursor.execute(
                    "INSERT INTO services(service_id, service_name, service_price) VALUES (%s, %s, %s)",
                    (
                        self.var_service_id.get(),
                        self.var_service_name.get(),
                        self.var_service_price.get(),
                    )
                )
                conn.commit()
                conn.close()
                self.fetch_data()
                messagebox.showinfo("Success", "Service Added Successfully!", parent=self.root)
                self.reset_data() # Reset form after adding
            except ValueError:
                messagebox.showerror("Invalid Input", "Service Price must be a number.", parent=self.root)
            except Exception as es:
                messagebox.showwarning("Warning", f"Something went wrong: {str(es)}", parent=self.root)

    def fetch_data(self):
        conn = mysql.connector.connect(host="localhost", username="root", password="11223344", database="hotel")
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT * FROM services")
        rows = my_cursor.fetchall()
        if len(rows) != 0:
            self.service_table.delete(*self.service_table.get_children())
            for i in rows:
                self.service_table.insert("", END, values=i)
        conn.close()

    def get_cursor(self, event=""):
        cursor_row = self.service_table.focus()
        content = self.service_table.item(cursor_row)
        row = content["values"]

        self.var_service_id.set(row[0])
        self.var_service_name.set(row[1])
        self.var_service_price.set(row[2])

    def update(self):
        if self.var_service_id.get() == "" or self.var_service_name.get() == "" or self.var_service_price.get() == "":
            messagebox.showerror("Error", "All fields are required for update.", parent=self.root)
        else:
            try:
                float(self.var_service_price.get()) # Validate price

                conn = mysql.connector.connect(host="localhost", username="root", password="11223344", database="hotel")
                my_cursor = conn.cursor()
                my_cursor.execute(
                    "UPDATE services SET service_name=%s, service_price=%s WHERE service_id=%s",
                    (
                        self.var_service_name.get(),
                        self.var_service_price.get(),
                        self.var_service_id.get(),
                    )
                )
                conn.commit()
                conn.close()
                self.fetch_data()
                messagebox.showinfo("Update", "Service details updated successfully!", parent=self.root)
                self.reset_data()
            except ValueError:
                messagebox.showerror("Invalid Input", "Service Price must be a number.", parent=self.root)
            except Exception as es:
                messagebox.showwarning("Warning", f"Something went wrong: {str(es)}", parent=self.root)

    def mDelete(self):
        mDelete_confirm = messagebox.askyesno("Hotel Management System", "Do you want to delete this service record?", parent=self.root)
        if mDelete_confirm:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="11223344", database="hotel")
                my_cursor = conn.cursor()
                query = "DELETE FROM services WHERE service_id=%s"
                value = (self.var_service_id.get(),)
                my_cursor.execute(query, value)
                conn.commit()
                conn.close()
                self.fetch_data()
                messagebox.showinfo("Delete", "Service record deleted successfully!", parent=self.root)
                self.reset_data()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete service record: {str(e)}", parent=self.root)

    def reset_data(self):
        self.var_service_name.set("")
        self.var_service_price.set("")
        # Generate new ID for next entry
        x = random.randint(100, 999)
        self.var_service_id.set(str(x))

if __name__ == '__main__':
    root = Tk()
    obj = Service_Win(root)
    root.mainloop()