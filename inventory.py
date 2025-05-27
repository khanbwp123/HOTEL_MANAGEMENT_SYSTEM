# inventory.py
from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
from datetime import datetime, date # For last_restocked_date
import random # For generating simple item IDs

class Inventory_Win:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System - Inventory Management")
        self.root.geometry("1200x600+230+220") # Adjusted geometry for inventory
        self.root.minsize(900, 500)
        self.root.resizable(True, True)

        # ======= Variables =======
        self.var_item_id = StringVar()
        x = random.randint(10000, 99999) # Generate a 5-digit ID
        self.var_item_id.set(str(x))

        self.var_item_name = StringVar()
        self.var_category = StringVar()
        self.var_quantity_on_hand = StringVar()
        self.var_unit_of_measure = StringVar()
        self.var_reorder_level = StringVar()
        self.var_last_restocked_date = StringVar(value=datetime.now().strftime("%d/%m/%Y"))
        self.var_supplier_id = StringVar() # Simple string for now, will link to Supplier entity later


        # ======= Title =======
        lbl_title = Label(self.root, text="HOTEL INVENTORY MANAGEMENT", font=("times new roman", 18, "bold"),
                          bg="black", fg="gold", bd=4, relief=RIDGE)
        lbl_title.place(x=0, y=0, width=1200, height=50)

        # ======= Left Frame (Form) =======
        labelframeleft = LabelFrame(self.root, bd=2, relief=RIDGE, text="Add/Update Inventory Item",
                                    font=("arial", 12, "bold"), padx=2)
        labelframeleft.place(x=5, y=50, width=450, height=500)

        # Item ID
        lbl_item_id = Label(labelframeleft, text="Item ID:", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_item_id.grid(row=0, column=0, sticky=W)
        enty_item_id = ttk.Entry(labelframeleft, textvariable=self.var_item_id, width=25,
                                  font=("arial", 13, "bold"), state="readonly")
        enty_item_id.grid(row=0, column=1, sticky=W)

        # Item Name
        lbl_item_name = Label(labelframeleft, text="Item Name:", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_item_name.grid(row=1, column=0, sticky=W)
        enty_item_name = ttk.Entry(labelframeleft, textvariable=self.var_item_name, width=25,
                                   font=("arial", 13, "bold"))
        enty_item_name.grid(row=1, column=1, sticky=W)

        # Category
        lbl_category = Label(labelframeleft, text="Category:", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_category.grid(row=2, column=0, sticky=W)
        combo_category = ttk.Combobox(labelframeleft, textvariable=self.var_category,
                                        font=("arial", 12, "bold"), width=23, state="readonly")
        combo_category["values"] = ("Housekeeping", "Minibar", "Restaurant", "Maintenance", "Office Supplies", "Other")
        combo_category.current(0)
        combo_category.grid(row=2, column=1, sticky=W)

        # Quantity on Hand
        lbl_quantity = Label(labelframeleft, text="Quantity on Hand:", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_quantity.grid(row=3, column=0, sticky=W)
        enty_quantity = ttk.Entry(labelframeleft, textvariable=self.var_quantity_on_hand, width=25,
                                  font=("arial", 13, "bold"))
        enty_quantity.grid(row=3, column=1, sticky=W)

        # Unit of Measure
        lbl_unit = Label(labelframeleft, text="Unit of Measure:", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_unit.grid(row=4, column=0, sticky=W)
        enty_unit = ttk.Entry(labelframeleft, textvariable=self.var_unit_of_measure, width=25,
                              font=("arial", 13, "bold"))
        enty_unit.grid(row=4, column=1, sticky=W)

        # Reorder Level
        lbl_reorder = Label(labelframeleft, text="Reorder Level:", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_reorder.grid(row=5, column=0, sticky=W)
        enty_reorder = ttk.Entry(labelframeleft, textvariable=self.var_reorder_level, width=25,
                                  font=("arial", 13, "bold"))
        enty_reorder.grid(row=5, column=1, sticky=W)

        # Last Restocked Date
        lbl_restocked_date = Label(labelframeleft, text="Last Restocked Date:", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_restocked_date.grid(row=6, column=0, sticky=W)
        enty_restocked_date = ttk.Entry(labelframeleft, textvariable=self.var_last_restocked_date, width=25,
                                        font=("arial", 13, "bold"), state="readonly")
        enty_restocked_date.grid(row=6, column=1, sticky=W)

        # Supplier ID
        lbl_supplier_id = Label(labelframeleft, text="Supplier ID:", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_supplier_id.grid(row=7, column=0, sticky=W)
        enty_supplier_id = ttk.Entry(labelframeleft, textvariable=self.var_supplier_id, width=25,
                                     font=("arial", 13, "bold"))
        enty_supplier_id.grid(row=7, column=1, sticky=W)


        # ======= Button Frame =======
        btn_frame = Frame(labelframeleft, bd=2, relief=RIDGE)
        btn_frame.place(x=0, y=420, width=440, height=40)

        Button(btn_frame, text="Add", command=self.add_data, font=("arial", 11, "bold"),
               bg="black", fg="gold", width=10).grid(row=0, column=0, padx=1)
        Button(btn_frame, text="UPDATE", command=self.update, font=("arial", 11, "bold"),
               bg="black", fg="gold", width=10).grid(row=0, column=1, padx=1)
        Button(btn_frame, text="DELETE", command=self.mDelete, font=("arial", 11, "bold"),
               bg="black", fg="gold", width=10).grid(row=0, column=2, padx=1)
        Button(btn_frame, text="RESET", command=self.reset_data, font=("arial", 11, "bold"),
               bg="black", fg="gold", width=9).grid(row=0, column=3, padx=1)

        # ======= Table Frame (Display Inventory) =======
        Table_Frame = LabelFrame(self.root, bd=2, relief=RIDGE, text="View Inventory Details",
                                 font=("arial", 12, "bold"), padx=2)
        Table_Frame.place(x=460, y=55, width=730, height=500)

        scroll_x = ttk.Scrollbar(Table_Frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(Table_Frame, orient=VERTICAL)

        self.inventory_table = ttk.Treeview(Table_Frame,
                                        columns=("id", "name", "category", "qty", "unit", "reorder", "restock_date", "supplier_id"),
                                        xscrollcommand=scroll_x.set,
                                        yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.inventory_table.xview)
        scroll_y.config(command=self.inventory_table.yview)

        self.inventory_table.heading("id", text="Item ID")
        self.inventory_table.heading("name", text="Name")
        self.inventory_table.heading("category", text="Category")
        self.inventory_table.heading("qty", text="Quantity")
        self.inventory_table.heading("unit", text="Unit")
        self.inventory_table.heading("reorder", text="Reorder Lvl")
        self.inventory_table.heading("restock_date", text="Restock Date")
        self.inventory_table.heading("supplier_id", text="Supplier ID")

        self.inventory_table["show"] = "headings"
        self.inventory_table.column("id", width=80)
        self.inventory_table.column("name", width=120)
        self.inventory_table.column("category", width=90)
        self.inventory_table.column("qty", width=70)
        self.inventory_table.column("unit", width=70)
        self.inventory_table.column("reorder", width=80)
        self.inventory_table.column("restock_date", width=100)
        self.inventory_table.column("supplier_id", width=80)

        self.inventory_table.pack(fill=BOTH, expand=1)

        self.inventory_table.bind("<ButtonRelease-1>", self.get_cursor)
        self.fetch_data() # Load existing inventory data on startup

    # ========== CRUD Operations ==========

    def add_data(self):
        if self.var_item_name.get() == "" or self.var_quantity_on_hand.get() == "":
            messagebox.showerror("ERROR", "Item Name and Quantity are required!", parent=self.root)
            return

        try:
            qty = int(self.var_quantity_on_hand.get())
            reorder = int(self.var_reorder_level.get() or 0) # Default to 0 if empty
        except ValueError:
            messagebox.showerror("Invalid Input", "Quantity and Reorder Level must be numbers.", parent=self.root)
            return

        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="11223344", database="hotel")
            my_cursor = conn.cursor()
            my_cursor.execute(
                "INSERT INTO inventory(item_id, item_name, category, quantity_on_hand, unit_of_measure, reorder_level, last_restocked_date, supplier_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    self.var_item_id.get(),
                    self.var_item_name.get(),
                    self.var_category.get(),
                    qty, # Use integer
                    self.var_unit_of_measure.get(),
                    reorder, # Use integer
                    datetime.strptime(self.var_last_restocked_date.get(), "%d/%m/%Y").date(),
                    self.var_supplier_id.get(),
                )
            )
            conn.commit()
            conn.close()
            self.fetch_data()
            messagebox.showinfo("Success", "Inventory Item Added Successfully!", parent=self.root)
            self.reset_data()
        except Exception as es:
            messagebox.showwarning("Warning", f"Something went wrong: {str(es)}", parent=self.root)

    def fetch_data(self):
        conn = mysql.connector.connect(host="localhost", username="root", password="11223344", database="hotel")
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT * FROM inventory")
        rows = my_cursor.fetchall()
        if len(rows) != 0:
            self.inventory_table.delete(*self.inventory_table.get_children())
            for i in rows:
                display_row = list(i)
                # Format date for display if it's a date object
                if hasattr(display_row[6], 'strftime'): # Index 6 is last_restocked_date
                    display_row[6] = display_row[6].strftime("%d/%m/%Y")
                self.inventory_table.insert("", END, values=display_row)
        conn.close()

    def get_cursor(self, event=""):
        cursor_row = self.inventory_table.focus()
        content = self.inventory_table.item(cursor_row)
        row = content["values"]

        self.var_item_id.set(row[0])
        self.var_item_name.set(row[1])
        self.var_category.set(row[2])
        self.var_quantity_on_hand.set(row[3])
        self.var_unit_of_measure.set(row[4])
        self.var_reorder_level.set(row[5])
        self.var_last_restocked_date.set(row[6])
        self.var_supplier_id.set(row[7])

    def update(self):
        if self.var_item_id.get() == "" or self.var_item_name.get() == "" or self.var_quantity_on_hand.get() == "":
            messagebox.showerror("Error", "Item ID, Name, and Quantity are required for update.", parent=self.root)
            return

        try:
            qty = int(self.var_quantity_on_hand.get())
            reorder = int(self.var_reorder_level.get() or 0)
        except ValueError:
            messagebox.showerror("Invalid Input", "Quantity and Reorder Level must be numbers.", parent=self.root)
            return

        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="11223344", database="hotel")
            my_cursor = conn.cursor()
            my_cursor.execute(
                "UPDATE inventory SET item_name=%s, category=%s, quantity_on_hand=%s, unit_of_measure=%s, reorder_level=%s, last_restocked_date=%s, supplier_id=%s WHERE item_id=%s",
                (
                    self.var_item_name.get(),
                    self.var_category.get(),
                    qty,
                    self.var_unit_of_measure.get(),
                    reorder,
                    datetime.strptime(self.var_last_restocked_date.get(), "%d/%m/%Y").date(),
                    self.var_supplier_id.get(),
                    self.var_item_id.get(),
                )
            )
            conn.commit()
            conn.close()
            self.fetch_data()
            messagebox.showinfo("Update", "Inventory item updated successfully!", parent=self.root)
            self.reset_data()
        except Exception as es:
            messagebox.showwarning("Warning", f"Something went wrong: {str(es)}", parent=self.root)

    def mDelete(self):
        mDelete_confirm = messagebox.askyesno("Hotel Management System", "Do you want to delete this inventory record?", parent=self.root)
        if mDelete_confirm:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="11223344", database="hotel")
                my_cursor = conn.cursor()
                query = "DELETE FROM inventory WHERE item_id=%s"
                value = (self.var_item_id.get(),)
                my_cursor.execute(query, value)
                conn.commit()
                conn.close()
                self.fetch_data()
                messagebox.showinfo("Delete", "Inventory record deleted successfully!", parent=self.root)
                self.reset_data()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete inventory record: {str(e)}", parent=self.root)

    def reset_data(self):
        self.var_item_name.set("")
        self.var_category.set("Housekeeping")
        self.var_quantity_on_hand.set("")
        self.var_unit_of_measure.set("")
        self.var_reorder_level.set("")
        self.var_last_restocked_date.set(datetime.now().strftime("%d/%m/%Y"))
        self.var_supplier_id.set("")
        # Generate new ID for next entry
        x = random.randint(10000, 99999)
        self.var_item_id.set(str(x))

if __name__ == '__main__':
    root = Tk()
    obj = Inventory_Win(root)
    root.mainloop()