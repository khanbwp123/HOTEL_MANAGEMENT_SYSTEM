# supplier.py
from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
import random

class Supplier_Win:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System - Suppliers")
        self.root.geometry("1000x500+230+220")

        self.var_supplier_id = StringVar()
        self.var_supplier_id.set(str(random.randint(1000, 9999)))
        self.var_name = StringVar()
        self.var_contact_person = StringVar()
        self.var_phone = StringVar()
        self.var_email = StringVar()
        self.var_address = StringVar()

        title = Label(self.root, text="SUPPLIER MANAGEMENT", font=("times new roman", 18, "bold"), bg="black", fg="gold", bd=4, relief=RIDGE)
        title.pack(side=TOP, fill=X)

        frame = LabelFrame(self.root, text="Add Supplier", font=("arial", 12, "bold"))
        frame.place(x=10, y=50, width=400, height=400)

        Label(frame, text="Supplier ID:", font=("arial", 12, "bold")).grid(row=0, column=0, padx=10, pady=5, sticky=W)
        Entry(frame, textvariable=self.var_supplier_id, state="readonly", font=("arial", 12)).grid(row=0, column=1, padx=10, pady=5)

        Label(frame, text="Name:", font=("arial", 12, "bold")).grid(row=1, column=0, padx=10, pady=5, sticky=W)
        Entry(frame, textvariable=self.var_name, font=("arial", 12)).grid(row=1, column=1, padx=10, pady=5)

        Label(frame, text="Contact Person:", font=("arial", 12, "bold")).grid(row=2, column=0, padx=10, pady=5, sticky=W)
        Entry(frame, textvariable=self.var_contact_person, font=("arial", 12)).grid(row=2, column=1, padx=10, pady=5)

        Label(frame, text="Phone:", font=("arial", 12, "bold")).grid(row=3, column=0, padx=10, pady=5, sticky=W)
        Entry(frame, textvariable=self.var_phone, font=("arial", 12)).grid(row=3, column=1, padx=10, pady=5)

        Label(frame, text="Email:", font=("arial", 12, "bold")).grid(row=4, column=0, padx=10, pady=5, sticky=W)
        Entry(frame, textvariable=self.var_email, font=("arial", 12)).grid(row=4, column=1, padx=10, pady=5)

        Label(frame, text="Address:", font=("arial", 12, "bold")).grid(row=5, column=0, padx=10, pady=5, sticky=W)
        Entry(frame, textvariable=self.var_address, font=("arial", 12)).grid(row=5, column=1, padx=10, pady=5)

        Button(frame, text="Add", command=self.add_data, font=("arial", 12, "bold"), bg="black", fg="gold").grid(row=6, column=0, padx=10, pady=10)
        Button(frame, text="Reset", command=self.reset_form, font=("arial", 12, "bold"), bg="black", fg="gold").grid(row=6, column=1, padx=10, pady=10)

        table_frame = Frame(self.root, bd=2, relief=RIDGE)
        table_frame.place(x=420, y=50, width=560, height=400)

        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(table_frame, orient=VERTICAL)
        self.supplier_table = ttk.Treeview(table_frame, columns=("id", "name", "contact", "phone", "email", "address"),
                                           xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.supplier_table.xview)
        scroll_y.config(command=self.supplier_table.yview)

        for col in ("id", "name", "contact", "phone", "email", "address"):
            self.supplier_table.heading(col, text=col.title())
            self.supplier_table.column(col, width=100)

        self.supplier_table["show"] = "headings"
        self.supplier_table.pack(fill=BOTH, expand=1)
        self.fetch_data()

    def add_data(self):
        if self.var_name.get() == "" or self.var_phone.get() == "":
            messagebox.showerror("Error", "Name and Phone are required", parent=self.root)
            return
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="11223344", database="hotel")
            my_cursor = conn.cursor()
            my_cursor.execute("INSERT INTO supplier VALUES(%s, %s, %s, %s, %s, %s)", (
                self.var_supplier_id.get(),
                self.var_name.get(),
                self.var_contact_person.get(),
                self.var_phone.get(),
                self.var_email.get(),
                self.var_address.get()
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Supplier added successfully", parent=self.root)
            self.fetch_data()
            self.reset_form()
        except Exception as es:
            messagebox.showerror("DB Error", f"Error due to: {str(es)}", parent=self.root)

    def fetch_data(self):
        conn = mysql.connector.connect(host="localhost", username="root", password="11223344", database="hotel")
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT * FROM supplier")
        rows = my_cursor.fetchall()
        if rows:
            self.supplier_table.delete(*self.supplier_table.get_children())
            for row in rows:
                self.supplier_table.insert("", END, values=row)
        conn.close()

    def reset_form(self):
        self.var_supplier_id.set(str(random.randint(1000, 9999)))
        self.var_name.set("")
        self.var_contact_person.set("")
        self.var_phone.set("")
        self.var_email.set("")
        self.var_address.set("")


if __name__ == '__main__':
    root = Tk()
    obj = Supplier_Win(root)
    root.mainloop()
