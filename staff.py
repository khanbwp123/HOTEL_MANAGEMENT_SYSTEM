# staff.py
from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
import random # For generating simple staff IDs

class Staff_Win:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System - Staff Details")
        self.root.geometry("1000x550+230+220") # Adjusted geometry for staff
        self.root.minsize(700, 450)
        self.root.resizable(True, True)

        # ======= Variables =======
        self.var_staff_id = StringVar()
        x = random.randint(10000, 99999) # Generate a 5-digit ID
        self.var_staff_id.set(str(x))

        self.var_staff_name = StringVar()
        self.var_staff_role = StringVar()


        # ======= Title =======
        lbl_title = Label(self.root, text="STAFF DETAILS", font=("times new roman", 18, "bold"),
                          bg="black", fg="gold", bd=4, relief=RIDGE)
        lbl_title.place(x=0, y=0, width=1000, height=50)

        # ======= Logo (Optional, you can remove if it clutters the staff window) =======
        img2 = Image.open(r"C:\Users\SAEEDCOMPUTERS\Downloads\img2.png") # Adjust path if needed
        img2 = img2.resize((100, 40), Image.Resampling.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)
        lblimg = Label(self.root, image=self.photoimg2, bd=0, relief=RIDGE)
        lblimg.place(x=5, y=2, width=100, height=40)

        # ======= Left Frame (Form) =======
        labelframeleft = LabelFrame(self.root, bd=2, relief=RIDGE, text="Add/Update Staff",
                                    font=("arial", 12, "bold"), padx=2)
        labelframeleft.place(x=5, y=50, width=450, height=250)

        # Staff ID
        lbl_staff_id = Label(labelframeleft, text="Staff ID:", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_staff_id.grid(row=0, column=0, sticky=W)
        enty_staff_id = ttk.Entry(labelframeleft, textvariable=self.var_staff_id, width=25,
                                  font=("arial", 13, "bold"), state="readonly") # ID is auto-generated
        enty_staff_id.grid(row=0, column=1, sticky=W)

        # Staff Name
        lbl_staff_name = Label(labelframeleft, text="Staff Name:", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_staff_name.grid(row=1, column=0, sticky=W)
        enty_staff_name = ttk.Entry(labelframeleft, textvariable=self.var_staff_name, width=25,
                                   font=("arial", 13, "bold"))
        enty_staff_name.grid(row=1, column=1, sticky=W)

        # Staff Role
        lbl_staff_role = Label(labelframeleft, text="Staff Role:", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_staff_role.grid(row=2, column=0, sticky=W)
        # Use Combobox for predefined roles for consistency
        combo_staff_role = ttk.Combobox(labelframeleft, textvariable=self.var_staff_role,
                                        font=("arial", 12, "bold"), width=23, state="readonly")
        combo_staff_role["values"] = ("Front Desk", "Housekeeping", "Restaurant Staff", "Manager", "Security", "Other")
        combo_staff_role.current(0)
        combo_staff_role.grid(row=2, column=1, sticky=W)

        # ======= Button Frame =======
        btn_frame = Frame(labelframeleft, bd=2, relief=RIDGE)
        btn_frame.place(x=0, y=180, width=440, height=40)

        Button(btn_frame, text="Add", command=self.add_data, font=("arial", 11, "bold"),
               bg="black", fg="gold", width=10).grid(row=0, column=0, padx=1)
        Button(btn_frame, text="UPDATE", command=self.update, font=("arial", 11, "bold"),
               bg="black", fg="gold", width=10).grid(row=0, column=1, padx=1)
        Button(btn_frame, text="DELETE", command=self.mDelete, font=("arial", 11, "bold"),
               bg="black", fg="gold", width=10).grid(row=0, column=2, padx=1)
        Button(btn_frame, text="RESET", command=self.reset_data, font=("arial", 11, "bold"),
               bg="black", fg="gold", width=9).grid(row=0, column=3, padx=1)

        # ======= Table Frame (Display Staff) =======
        Table_Frame = LabelFrame(self.root, bd=2, relief=RIDGE, text="View Staff Details",
                                 font=("arial", 12, "bold"), padx=2)
        Table_Frame.place(x=460, y=55, width=530, height=450)

        scroll_x = ttk.Scrollbar(Table_Frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(Table_Frame, orient=VERTICAL)

        self.staff_table = ttk.Treeview(Table_Frame,
                                        columns=("staff_id", "staff_name", "staff_role"),
                                        xscrollcommand=scroll_x.set,
                                        yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.staff_table.xview)
        scroll_y.config(command=self.staff_table.yview)

        self.staff_table.heading("staff_id", text="Staff ID")
        self.staff_table.heading("staff_name", text="Name")
        self.staff_table.heading("staff_role", text="Role")

        self.staff_table["show"] = "headings"
        self.staff_table.column("staff_id", width=100)
        self.staff_table.column("staff_name", width=150)
        self.staff_table.column("staff_role", width=150)

        self.staff_table.pack(fill=BOTH, expand=1)

        self.staff_table.bind("<ButtonRelease-1>", self.get_cursor)
        self.fetch_data() # Load existing staff data on startup

    # ========== CRUD Operations ==========

    def add_data(self):
        if self.var_staff_name.get() == "" or self.var_staff_role.get() == "":
            messagebox.showerror("ERROR", "Name and Role are required!", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="11223344", database="hotel")
                my_cursor = conn.cursor()
                my_cursor.execute(
                    "INSERT INTO staff(staff_id, staff_name, staff_role) VALUES (%s, %s, %s)",
                    (
                        self.var_staff_id.get(),
                        self.var_staff_name.get(),
                        self.var_staff_role.get(),
                    )
                )
                conn.commit()
                conn.close()
                self.fetch_data()
                messagebox.showinfo("Success", "Staff Added Successfully!", parent=self.root)
                self.reset_data() # Reset form after adding
            except Exception as es:
                messagebox.showwarning("Warning", f"Something went wrong: {str(es)}", parent=self.root)

    def fetch_data(self):
        conn = mysql.connector.connect(host="localhost", username="root", password="11223344", database="hotel")
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT * FROM staff")
        rows = my_cursor.fetchall()
        if len(rows) != 0:
            self.staff_table.delete(*self.staff_table.get_children())
            for i in rows:
                self.staff_table.insert("", END, values=i)
        conn.close()

    def get_cursor(self, event=""):
        cursor_row = self.staff_table.focus()
        content = self.staff_table.item(cursor_row)
        row = content["values"]

        self.var_staff_id.set(row[0])
        self.var_staff_name.set(row[1])
        self.var_staff_role.set(row[2])

    def update(self):
        if self.var_staff_id.get() == "" or self.var_staff_name.get() == "" or self.var_staff_role.get() == "":
            messagebox.showerror("Error", "All fields are required for update.", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="11223344", database="hotel")
                my_cursor = conn.cursor()
                my_cursor.execute(
                    "UPDATE staff SET staff_name=%s, staff_role=%s WHERE staff_id=%s",
                    (
                        self.var_staff_name.get(),
                        self.var_staff_role.get(),
                        self.var_staff_id.get(),
                    )
                )
                conn.commit()
                conn.close()
                self.fetch_data()
                messagebox.showinfo("Update", "Staff details updated successfully!", parent=self.root)
                self.reset_data() # Reset form after updating
            except Exception as es:
                messagebox.showwarning("Warning", f"Something went wrong: {str(es)}", parent=self.root)

    def mDelete(self):
        mDelete_confirm = messagebox.askyesno("Hotel Management System", "Do you want to delete this staff record?", parent=self.root)
        if mDelete_confirm:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="11223344", database="hotel")
                my_cursor = conn.cursor()
                query = "DELETE FROM staff WHERE staff_id=%s"
                value = (self.var_staff_id.get(),)
                my_cursor.execute(query, value)
                conn.commit()
                conn.close()
                self.fetch_data()
                messagebox.showinfo("Delete", "Staff record deleted successfully!", parent=self.root)
                self.reset_data() # Reset form after deleting
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete staff record: {str(e)}", parent=self.root)

    def reset_data(self):
        self.var_staff_name.set("")
        self.var_staff_role.set("Front Desk") # Reset to default role
        # Generate new ID for next entry
        x = random.randint(10000, 99999)
        self.var_staff_id.set(str(x))

if __name__ == '__main__':
    root = Tk()
    obj = Staff_Win(root)
    root.mainloop()