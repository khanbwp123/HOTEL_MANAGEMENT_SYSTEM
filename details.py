from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from time import strftime
from _datetime import datetime
import mysql.connector
from tkinter import messagebox

class Details_Room:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("1295x550+230+220")
        self.root.minsize(800, 500)
        self.root.resizable(True, True)

        # ======= Title =======
        lbl_title = Label(self.root, text="NEW ROOM DETAILS", font=("times new roman", 18, "bold"),
                          bg="black", fg="gold", bd=4, relief=RIDGE)
        lbl_title.place(x=0, y=0, width=1295, height=50)

        # ======= Logo =======
        img2 = Image.open(r"C:\Users\SAEEDCOMPUTERS\Downloads\img2.png")
        img2 = img2.resize((100, 40), Image.Resampling.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)
        lblimg = Label(self.root, image=self.photoimg2, bd=0, relief=RIDGE)
        lblimg.place(x=5, y=2, width=100, height=40)

        # ======= Variables =======
        self.var_floor = StringVar()
        self.var_roomno = StringVar()
        self.var_roomtype = StringVar()

        # ======= Left Frame (Form) =======
        labelframeleft = LabelFrame(self.root, bd=2, relief=RIDGE, text="New Room Add",
                                    font=("arial", 12, "bold"), padx=2)
        labelframeleft.place(x=5, y=50, width=540, height=350)

        # Floor
        lbl_floor = Label(labelframeleft, text="Floor", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_floor.grid(row=0, column=0, sticky=W)
        enty_floor = ttk.Entry(labelframeleft, textvariable=self.var_floor, width=20, font=("arial", 13, "bold"))
        enty_floor.grid(row=0, column=1, sticky=W)

        # Room Number
        lbl_RoomNo = Label(labelframeleft, text="Room No.", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_RoomNo.grid(row=1, column=0, sticky=W)
        enty_RoomNo = ttk.Entry(labelframeleft, textvariable=self.var_roomno, width=20, font=("arial", 13, "bold"))
        enty_RoomNo.grid(row=1, column=1, sticky=W, padx=20)

        # Room Type
        lbl_RoomType = Label(labelframeleft, text="Room Type :", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_RoomType.grid(row=2, column=0, sticky=W, padx=20)
        enty_RoomType = ttk.Entry(labelframeleft, textvariable=self.var_roomtype, width=20, font=("arial", 13, "bold"))
        enty_RoomType.grid(row=2, column=1, sticky=W, padx=20)

        # ======= Button Frame =======
        btn_frame = Frame(labelframeleft, bd=2, relief=RIDGE)
        btn_frame.place(x=0, y=200, width=412, height=40)

        Button(btn_frame, text="Add", command=self.add_data, font=("arial", 11, "bold"),
               bg="black", fg="gold", width=10).grid(row=0, column=0, padx=1)
        Button(btn_frame, text="UPDATE",command=self.update,font=("arial", 11, "bold"),
               bg="black", fg="gold", width=10).grid(row=0, column=1, padx=1)
        Button(btn_frame, text="DELETE",command=self.mDelete,font=("arial", 11, "bold"),
               bg="black", fg="gold", width=10).grid(row=0, column=2, padx=1)
        Button(btn_frame, text="RESET",command=self.reset_data,font=("arial", 11, "bold"),
               bg="black", fg="gold", width=9).grid(row=0, column=3, padx=1)

        # ======= Table Frame =======
        Table_Frame = LabelFrame(self.root, bd=2, relief=RIDGE, text="SHOW ROOM DETAILS",
                                 font=("arial", 12, "bold"), padx=2)
        Table_Frame.place(x=600, y=55, width=600, height=350)

        scroll_x = ttk.Scrollbar(Table_Frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(Table_Frame, orient=VERTICAL)

        self.room_table = ttk.Treeview(Table_Frame,
                                       columns=("floor", "roomno", "roomtype"),
                                       xscrollcommand=scroll_x.set,
                                       yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.room_table.xview)
        scroll_y.config(command=self.room_table.yview)

        self.room_table.heading("floor", text="Floor")
        self.room_table.heading("roomno", text="Room No.")
        self.room_table.heading("roomtype", text="Room Type")

        self.room_table["show"] = "headings"
        self.room_table.column("floor", width=100)
        self.room_table.column("roomno", width=100)
        self.room_table.column("roomtype", width=100)

        self.room_table.pack(fill=BOTH, expand=1)

        # Fetch existing data on load
        self.room_table.bind("<ButtonRelease-1>", self.get_cursor)
        self.fetch_data()


    # ========== Add Data ==========
    def add_data(self):
        if self.var_floor.get() == "" or self.var_roomtype.get() == "":
            messagebox.showerror("ERROR", "All fields are required")
        else:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="11223344", database="hotel")
                my_cursor = conn.cursor()
                my_cursor.execute(
                    "INSERT INTO details(floor, roomno, roomtype) VALUES (%s, %s, %s)",
                    (
                        self.var_floor.get(),
                        self.var_roomno.get(),
                        self.var_roomtype.get(),
                    )
                )
                conn.commit()
                conn.close()
                self.fetch_data()
                messagebox.showinfo("Success", "New Room Added", parent=self.root)
            except Exception as es:
                messagebox.showwarning("Warning", f"Something went wrong: {str(es)}", parent=self.root)

    # ========== Fetch Data ==========
    def fetch_data(self):
        conn = mysql.connector.connect(host="localhost", username="root", password="11223344", database="hotel")
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT * FROM details")
        rows = my_cursor.fetchall()
        if len(rows) != 0:
            self.room_table.delete(*self.room_table.get_children())
            for i in rows:
                self.room_table.insert("", END, values=i)
        conn.close()

    def get_cursor(self, event=""):
        cursor_row = self.room_table.focus()
        content = self.room_table.item(cursor_row)
        row = content["values"]

        self.var_floor.set(row[0]),
        self.var_roomno.set(row[1]),
        self.var_roomtype.set(row[2])

    def update(self):
        if self.var_floor.get() == "":
            messagebox.showerror("Error", "Please enter floor number", parent=self.root)
        else:
            conn = mysql.connector.connect(host="localhost", username="root", password="11223344", database="hotel")
            my_cursor = conn.cursor()
            my_cursor.execute(
                "update details set floor=%s,roomtype=%s where roomno=%s",
                (      self.var_floor.get(),
                               self.var_roomtype.get(),
                               self.var_roomno.get(),
                ))
        conn.commit()
        self.fetch_data()
        conn.close()
        messagebox.showinfo("Update", "New room details are updated successfully", parent=self.root)

    #delete

    def mDelete(self):
        mDelete = messagebox.askyesno("Hotel Management System", "Do you want to delete this room?", parent=self.root)
        if mDelete > 0:
            conn = mysql.connector.connect(host="localhost", username="root", password="11223344", database="hotel")
            my_cursor = conn.cursor()
            query = "DELETE FROM details WHERE roomno=%s"
            value = (self.var_roomno.get(),)  # The comma makes it a tuple, even with one element
            my_cursor.execute(query, value)
        else:
            if not mDelete:
                return

        conn.commit()
        self.fetch_data()
        conn.close()
        messagebox.showinfo("Delete", "Room has been successfully deleted!", parent=self.root)

    def reset_data(self):
        self.var_floor.set(""),
        self.var_roomno.set(""),
        self.var_roomtype.set("")



if __name__ == '__main__':
    root = Tk()
    obj = Details_Room(root)
    root.mainloop()
