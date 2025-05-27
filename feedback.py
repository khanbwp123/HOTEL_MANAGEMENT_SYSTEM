# feedback.py
from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
from datetime import datetime, date # KEEP THIS IMPORT as it is vital for datetime.strptime elsewhere
import random

class Feedback_Win:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System - Guest Feedback")
        self.root.geometry("1100x550+230+220")
        self.root.minsize(800, 500)
        self.root.resizable(True, True)

        # ======= Variables =======
        self.var_feedback_id = StringVar()
        x = random.randint(1000, 9999) # Generate a 4-digit ID
        self.var_feedback_id.set(str(x))

        self.var_booking_id = StringVar()
        self.var_guest_contact = StringVar() # To link to customer indirectly
        self.var_feedback_type = StringVar() # Complaint or Suggestion/Compliment
        self.var_comments = StringVar()
        self.var_feedback_date = StringVar(value=datetime.now().strftime("%d/%m/%Y")) # Default to today
        self.var_resolution_status = StringVar() # Pending, In Progress, Resolved, Closed


        # ======= Title =======
        lbl_title = Label(self.root, text="GUEST FEEDBACK & COMPLAINTS", font=("times new roman", 18, "bold"),
                          bg="black", fg="gold", bd=4, relief=RIDGE)
        lbl_title.place(x=0, y=0, width=1100, height=50)

        # ======= Left Frame (Form) =======
        labelframeleft = LabelFrame(self.root, bd=2, relief=RIDGE, text="Feedback Details",
                                    font=("arial", 12, "bold"), padx=2)
        labelframeleft.place(x=5, y=50, width=450, height=450)

        # Feedback ID
        lbl_feedback_id = Label(labelframeleft, text="Feedback ID:", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_feedback_id.grid(row=0, column=0, sticky=W)
        enty_feedback_id = ttk.Entry(labelframeleft, textvariable=self.var_feedback_id, width=25,
                                     font=("arial", 13, "bold"), state="readonly")
        enty_feedback_id.grid(row=0, column=1, sticky=W)

        # Booking ID (Optional link to a specific booking)
        lbl_booking_id = Label(labelframeleft, text="Booking ID (Optional):", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_booking_id.grid(row=1, column=0, sticky=W)
        enty_booking_id = ttk.Entry(labelframeleft, textvariable=self.var_booking_id, width=25,
                                    font=("arial", 13, "bold"))
        enty_booking_id.grid(row=1, column=1, sticky=W)

        # Guest Contact (to link to customer indirectly)
        lbl_guest_contact = Label(labelframeleft, text="Guest Contact No.:", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_guest_contact.grid(row=2, column=0, sticky=W)
        enty_guest_contact = ttk.Entry(labelframeleft, textvariable=self.var_guest_contact, width=25,
                                       font=("arial", 13, "bold"))
        enty_guest_contact.grid(row=2, column=1, sticky=W)

        # Feedback Type (Combobox)
        lbl_feedback_type = Label(labelframeleft, text="Feedback Type:", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_feedback_type.grid(row=3, column=0, sticky=W)
        combo_feedback_type = ttk.Combobox(labelframeleft, textvariable=self.var_feedback_type,
                                           font=("arial", 12, "bold"), width=23, state="readonly")
        combo_feedback_type["values"] = ("Complaint", "Suggestion", "Compliment", "Query")
        combo_feedback_type.current(0)
        combo_feedback_type.grid(row=3, column=1, sticky=W)

        # Comments (Text Area for longer input)
        lbl_comments = Label(labelframeleft, text="Comments:", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_comments.grid(row=4, column=0, sticky=W)
        self.txt_comments = Text(labelframeleft, width=25, height=5, font=("arial", 11))
        self.txt_comments.grid(row=4, column=1, sticky=W, padx=2)
        self.txt_comments.bind("<KeyRelease>", self.update_comments_var)

        # Feedback Date (Readonly, auto-filled)
        lbl_feedback_date = Label(labelframeleft, text="Feedback Date:", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_feedback_date.grid(row=5, column=0, sticky=W)
        enty_feedback_date = ttk.Entry(labelframeleft, textvariable=self.var_feedback_date, width=25,
                                       font=("arial", 13, "bold"), state="readonly")
        enty_feedback_date.grid(row=5, column=1, sticky=W)

        # Resolution Status (Combobox)
        lbl_resolution_status = Label(labelframeleft, text="Resolution Status:", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_resolution_status.grid(row=6, column=0, sticky=W)
        combo_resolution_status = ttk.Combobox(labelframeleft, textvariable=self.var_resolution_status,
                                               font=("arial", 12, "bold"), width=23, state="readonly")
        combo_resolution_status["values"] = ("Pending", "In Progress", "Resolved", "Closed")
        combo_resolution_status.current(0)
        combo_resolution_status.grid(row=6, column=1, sticky=W)


        # ======= Button Frame =======
        btn_frame = Frame(labelframeleft, bd=2, relief=RIDGE)
        btn_frame.place(x=0, y=380, width=440, height=40)

        Button(btn_frame, text="Add", command=self.add_data, font=("arial", 11, "bold"),
               bg="black", fg="gold", width=10).grid(row=0, column=0, padx=1)
        Button(btn_frame, text="UPDATE", command=self.update, font=("arial", 11, "bold"),
               bg="black", fg="gold", width=10).grid(row=0, column=1, padx=1)
        Button(btn_frame, text="DELETE", command=self.mDelete, font=("arial", 11, "bold"),
               bg="black", fg="gold", width=10).grid(row=0, column=2, padx=1)
        Button(btn_frame, text="RESET", command=self.reset_data, font=("arial", 11, "bold"),
               bg="black", fg="gold", width=9).grid(row=0, column=3, padx=1)

        # --- NEW: Image on the right side (EXPANDED HORIZONTALLY) ---
        self.photoimg_feedback = None # Initialize to None in case loading fails
        try:
            # IMPORTANT: Confirm this path is absolutely correct and the image file exists.
            img_feedback = Image.open(r"C:\Users\SAEEDCOMPUTERS\Downloads\feedback.jpg")
            # Increased width to 620, keeping height at 150 for a rectangular look
            img_feedback = img_feedback.resize((620, 150), Image.Resampling.LANCZOS)
            self.photoimg_feedback = ImageTk.PhotoImage(img_feedback)

            lbl_img_feedback = Label(self.root, image=self.photoimg_feedback, bd=4, relief=RIDGE)
            # Place with new dimensions. X-position kept similar to align with the left frame's right edge.
            lbl_img_feedback.place(x=465, y=55, width=620, height=150)
            print("Feedback_Win: Image loaded and placed successfully.")
        except FileNotFoundError:
            messagebox.showerror("Image Error",
                                 "Feedback image not found! Check path: C:\\Users\\SAEEDCOMPUTERS\\Downloads\\feedback.jpg",
                                 parent=self.root)
            print("Feedback_Win: Image file not found error occurred.")
        except Exception as e:
            messagebox.showerror("Image Error", f"Error loading feedback image: {str(e)}", parent=self.root)
            print(f"Feedback_Win: Generic error loading image: {e}")

        # ======= Table Frame (Display Feedback) =======
        # Adjusted X position to make space for the image
        Table_Frame = LabelFrame(self.root, bd=2, relief=RIDGE, text="View All Feedback",
                                 font=("arial", 12, "bold"), padx=2)
        Table_Frame.place(x=460, y=210, width=630, height=295) # This position is already good for this layout

        scroll_x = ttk.Scrollbar(Table_Frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(Table_Frame, orient=VERTICAL)

        self.feedback_table = ttk.Treeview(Table_Frame,
                                           columns=("id", "booking_id", "guest_contact", "type", "comments", "date", "status"),
                                           xscrollcommand=scroll_x.set,
                                           yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.feedback_table.xview)
        scroll_y.config(command=self.feedback_table.yview)

        self.feedback_table.heading("id", text="Fbk ID")
        self.feedback_table.heading("booking_id", text="Booking ID")
        self.feedback_table.heading("guest_contact", text="Guest Contact")
        self.feedback_table.heading("type", text="Type")
        self.feedback_table.heading("comments", text="Comments")
        self.feedback_table.heading("date", text="Date")
        self.feedback_table.heading("status", text="Status")

        self.feedback_table["show"] = "headings"
        self.feedback_table.column("id", width=60)
        self.feedback_table.column("booking_id", width=80)
        self.feedback_table.column("guest_contact", width=100)
        self.feedback_table.column("type", width=80)
        self.feedback_table.column("comments", width=200)
        self.feedback_table.column("date", width=80)
        self.feedback_table.column("status", width=80)

        self.feedback_table.pack(fill=BOTH, expand=1)

        self.feedback_table.bind("<ButtonRelease-1>", self.get_cursor)
        self.fetch_data() # Load existing feedback data on startup

    # Helper to update StringVar from Text widget
    def update_comments_var(self, event=None):
        self.var_comments.set(self.txt_comments.get("1.0", END).strip())

    # ========== CRUD Operations ==========

    def add_data(self):
        self.update_comments_var() # Ensure comments var is updated
        if self.var_guest_contact.get() == "" or self.var_comments.get() == "" or self.var_feedback_type.get() == "":
            messagebox.showerror("ERROR", "Guest Contact, Feedback Type, and Comments are required!", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="11223344", database="hotel")
                my_cursor = conn.cursor()
                my_cursor.execute(
                    "INSERT INTO guest_feedback(feedback_id, booking_id, guest_contact, feedback_type, comments, feedback_date, resolution_status) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (
                        self.var_feedback_id.get(),
                        self.var_booking_id.get() if self.var_booking_id.get() else None,
                        self.var_guest_contact.get(),
                        self.var_feedback_type.get(),
                        self.var_comments.get(),
                        datetime.strptime(self.var_feedback_date.get(), "%d/%m/%Y").date(),
                        self.var_resolution_status.get(),
                    )
                )
                conn.commit()
                conn.close()
                self.fetch_data()
                messagebox.showinfo("Success", "Feedback Submitted Successfully!", parent=self.root)
                self.reset_data()
            except Exception as es:
                messagebox.showwarning("Warning", f"Something went wrong: {str(es)}", parent=self.root)

    def fetch_data(self):
        conn = mysql.connector.connect(host="localhost", username="root", password="11223344", database="hotel")
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT * FROM guest_feedback")
        rows = my_cursor.fetchall()
        if len(rows) != 0:
            self.feedback_table.delete(*self.feedback_table.get_children())
            for i in rows:
                display_row = list(i)
                # --- START OF THE FIX ---
                # Changed from isinstance(display_row[5], datetime.date)
                # to hasattr(display_row[5], 'strftime') for robustness
                if hasattr(display_row[5], 'strftime'):
                    display_row[5] = display_row[5].strftime("%d/%m/%Y")
                # --- END OF THE FIX ---
                self.feedback_table.insert("", END, values=display_row)
        conn.close()

    def get_cursor(self, event=""):
        cursor_row = self.feedback_table.focus()
        content = self.feedback_table.item(cursor_row)
        row = content["values"]

        self.var_feedback_id.set(row[0])
        self.var_booking_id.set(row[1])
        self.var_guest_contact.set(row[2])
        self.var_feedback_type.set(row[3])
        self.var_comments.set(row[4])
        self.txt_comments.delete("1.0", END)
        self.txt_comments.insert("1.0", row[4])
        self.var_feedback_date.set(row[5])
        self.var_resolution_status.set(row[6])

    def update(self):
        self.update_comments_var()
        if self.var_feedback_id.get() == "" or self.var_guest_contact.get() == "" or self.var_comments.get() == "" or self.var_feedback_type.get() == "":
            messagebox.showerror("Error", "Feedback ID, Guest Contact, Type, and Comments are required for update.", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="11223344", database="hotel")
                my_cursor = conn.cursor()
                my_cursor.execute(
                    "UPDATE guest_feedback SET booking_id=%s, guest_contact=%s, feedback_type=%s, comments=%s, feedback_date=%s, resolution_status=%s WHERE feedback_id=%s",
                    (
                        self.var_booking_id.get() if self.var_booking_id.get() else None,
                        self.var_guest_contact.get(),
                        self.var_feedback_type.get(),
                        self.var_comments.get(),
                        datetime.strptime(self.var_feedback_date.get(), "%d/%m/%Y").date(),
                        self.var_resolution_status.get(),
                        self.var_feedback_id.get(),
                    )
                )
                conn.commit()
                conn.close()
                self.fetch_data()
                messagebox.showinfo("Update", "Feedback details updated successfully!", parent=self.root)
                self.reset_data()
            except Exception as es:
                messagebox.showwarning("Warning", f"Something went wrong: {str(es)}", parent=self.root)

    def mDelete(self):
        mDelete_confirm = messagebox.askyesno("Hotel Management System", "Do you want to delete this feedback record?", parent=self.root)
        if mDelete_confirm:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="11223344", database="hotel")
                my_cursor = conn.cursor()
                query = "DELETE FROM guest_feedback WHERE feedback_id=%s"
                value = (self.var_feedback_id.get(),)
                my_cursor.execute(query, value)
                conn.commit()
                conn.close()
                self.fetch_data()
                messagebox.showinfo("Delete", "Feedback record deleted successfully!", parent=self.root)
                self.reset_data()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete feedback record: {str(e)}", parent=self.root)

    def reset_data(self):
        self.var_booking_id.set("")
        self.var_guest_contact.set("")
        self.var_feedback_type.set("Complaint")
        self.var_comments.set("")
        self.txt_comments.delete("1.0", END)
        self.var_feedback_date.set(datetime.now().strftime("%d/%m/%Y"))
        self.var_resolution_status.set("Pending")
        # Generate new ID for next entry
        x = random.randint(1000, 9999)
        self.var_feedback_id.set(str(x))

if __name__ == '__main__':
    root = Tk()
    obj = Feedback_Win(root)
    root.mainloop()