# payment.py
from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

class PaymentWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Payment Processing")
        self.root.geometry("800x500+300+150")
        self.root.resizable(False, False)

        # ====== Variables ======
        self.var_booking_ref = StringVar()
        self.var_payment_amount = StringVar()
        self.var_payment_method = StringVar()
        self.var_due_amount = StringVar(value="0.0") # To show pending amount
        self.var_total_booking_amount = StringVar(value="0.0") # To show total booking amount

        # ======= Title ========
        lbl_title = Label(self.root, text="PROCESS PAYMENTS", font=("times new roman", 20, "bold"), bg="black",
                          fg="gold", bd=4, relief=RIDGE)
        lbl_title.pack(side=TOP, fill=X)

        # ======== Labelframe (Left Side) ======
        labelframe = LabelFrame(self.root, bd=2, relief=RIDGE, text="Payment Details", font=("arial", 12, "bold"), padx=5)
        labelframe.place(x=10, y=60, width=380, height=430)

        # Booking Reference
        lbl_booking_ref = Label(labelframe, text="Booking Ref:", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_booking_ref.grid(row=0, column=0, sticky=W)
        self.entry_booking_ref = ttk.Entry(labelframe, textvariable=self.var_booking_ref, width=25, font=("arial", 13, "bold"))
        self.entry_booking_ref.grid(row=0, column=1, sticky=W)
        self.entry_booking_ref.bind("<Leave>", self.fetch_booking_details) # Fetch details on leaving the entry

        # Fetch Booking Details Button (Optional, can rely on bind)
        btn_fetch_booking = Button(labelframe, text="Fetch Booking", command=self.fetch_booking_details, font=("arial", 10, "bold"), bg="blue", fg="white")
        btn_fetch_booking.grid(row=0, column=2, padx=5)


        # Total Booking Amount (Readonly)
        lbl_total_booking_amount = Label(labelframe, text="Total Booking Amt:", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_total_booking_amount.grid(row=1, column=0, sticky=W)
        entry_total_booking_amount = ttk.Entry(labelframe, textvariable=self.var_total_booking_amount, width=25, font=("arial", 13, "bold"), state="readonly")
        entry_total_booking_amount.grid(row=1, column=1, sticky=W)

        # Due Amount (Readonly)
        lbl_due_amount = Label(labelframe, text="Due Amount:", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_due_amount.grid(row=2, column=0, sticky=W)
        entry_due_amount = ttk.Entry(labelframe, textvariable=self.var_due_amount, width=25, font=("arial", 13, "bold"), state="readonly")
        entry_due_amount.grid(row=2, column=1, sticky=W)

        # Payment Amount
        lbl_payment_amount = Label(labelframe, text="Payment Amount:", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_payment_amount.grid(row=3, column=0, sticky=W)
        entry_payment_amount = ttk.Entry(labelframe, textvariable=self.var_payment_amount, width=25, font=("arial", 13, "bold"))
        entry_payment_amount.grid(row=3, column=1, sticky=W)

        # Payment Method
        lbl_payment_method = Label(labelframe, text="Payment Method:", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_payment_method.grid(row=4, column=0, sticky=W)
        combo_payment_method = ttk.Combobox(labelframe, textvariable=self.var_payment_method, font=("arial", 12, "bold"), width=23, state="readonly")
        combo_payment_method["values"] = ("Cash", "Credit Card", "Debit Card", "Online Transfer", "Mobile Pay")
        combo_payment_method.set("Cash")
        combo_payment_method.grid(row=4, column=1, sticky=W)

        # Buttons Frame
        btn_frame = Frame(labelframe, bd=2, relief=RIDGE)
        btn_frame.place(x=0, y=300, width=370, height=40)

        btn_add = Button(btn_frame, text="Add Payment", command=self.add_payment, font=("arial", 11, "bold"), bg="black", fg="gold", width=12)
        btn_add.grid(row=0, column=0, padx=1)

        btn_clear = Button(btn_frame, text="Clear", command=self.clear_fields, font=("arial", 11, "bold"), bg="black", fg="gold", width=12)
        btn_clear.grid(row=0, column=1, padx=1)


        # ======= Table Frame (Right Side) ======
        table_frame = LabelFrame(self.root, bd=2, relief=RIDGE, text="Recent Payments", font=("arial", 12, "bold"), padx=2)
        table_frame.place(x=400, y=60, width=390, height=430)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.payment_table = ttk.Treeview(table_frame, column=("payment_id", "booking_ref", "amount", "date", "method"),
                                          xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.payment_table.xview)
        scroll_y.config(command=self.payment_table.yview)

        self.payment_table.heading("payment_id", text="ID")
        self.payment_table.heading("booking_ref", text="Booking Ref")
        self.payment_table.heading("amount", text="Amount")
        self.payment_table.heading("date", text="Date")
        self.payment_table.heading("method", text="Method")

        self.payment_table["show"] = "headings"

        self.payment_table.column("payment_id", width=50)
        self.payment_table.column("booking_ref", width=80)
        self.payment_table.column("amount", width=80)
        self.payment_table.column("date", width=120)
        self.payment_table.column("method", width=80)

        self.payment_table.pack(fill=BOTH, expand=1)
        self.payment_table.bind("<ButtonRelease-1>", self.get_cursor)
        self.fetch_all_payments() # Load payments on start

    def fetch_booking_details(self, event=None):
        booking_ref = self.var_booking_ref.get()
        if not booking_ref:
            self.var_total_booking_amount.set("0.0")
            self.var_due_amount.set("0.0")
            return

        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="11223344", database="hotel")
            my_cursor = conn.cursor()

            # Get TotalAmount from room table
            my_cursor.execute("SELECT TotalAmount FROM room WHERE Ref = %s", (booking_ref,))
            result = my_cursor.fetchone()

            if result:
                total_amount = float(result[0])
                self.var_total_booking_amount.set(f"{total_amount:.2f}")

                # Calculate sum of payments made for this booking
                my_cursor.execute("SELECT SUM(payment_amount) FROM payment WHERE booking_ref = %s", (booking_ref,))
                paid_amount_result = my_cursor.fetchone()
                paid_amount = float(paid_amount_result[0]) if paid_amount_result and paid_amount_result[0] else 0.0

                due_amount = total_amount - paid_amount
                self.var_due_amount.set(f"{due_amount:.2f}")

            else:
                messagebox.showerror("Error", "Booking Reference not found!", parent=self.root)
                self.var_total_booking_amount.set("0.0")
                self.var_due_amount.set("0.0")
            conn.close()

        except Exception as e:
            messagebox.showerror("DB Error", f"Error fetching booking details: {str(e)}", parent=self.root)
            self.var_total_booking_amount.set("0.0")
            self.var_due_amount.set("0.0")

    def add_payment(self):
        booking_ref = self.var_booking_ref.get()
        payment_amount_str = self.var_payment_amount.get()
        payment_method = self.var_payment_method.get()

        if not booking_ref or not payment_amount_str or not payment_method:
            messagebox.showerror("Error", "All fields are required!", parent=self.root)
            return

        try:
            payment_amount = float(payment_amount_str)
            if payment_amount <= 0:
                messagebox.showerror("Invalid Amount", "Payment amount must be positive.", parent=self.root)
                return
        except ValueError:
            messagebox.showerror("Invalid Amount", "Payment amount must be a number.", parent=self.root)
            return

        # Optional: Check if payment amount exceeds due amount
        total_booking_amount = float(self.var_total_booking_amount.get())
        current_due_amount = float(self.var_due_amount.get())

        if payment_amount > current_due_amount and current_due_amount > 0:
            confirm = messagebox.askyesno("Confirm Payment",
                                          f"Payment amount ({payment_amount:.2f}) exceeds due amount ({current_due_amount:.2f}). "
                                          f"Do you want to proceed with overpayment?", parent=self.root)
            if not confirm:
                return


        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="11223344", database="hotel")
            my_cursor = conn.cursor()

            query = "INSERT INTO payment (booking_ref, payment_amount, payment_method) VALUES (%s, %s, %s)"
            values = (booking_ref, payment_amount, payment_method)
            my_cursor.execute(query, values)
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Payment recorded successfully!", parent=self.root)
            self.clear_fields()
            self.fetch_all_payments()
            # The trigger (to be created) will update room status automatically
        except mysql.connector.Error as err:
            if err.errno == 1452: # Foreign key constraint fails
                 messagebox.showerror("Database Error", "Invalid Booking Reference. Please enter a valid booking ID.", parent=self.root)
            else:
                messagebox.showerror("Database Error", f"Failed to add payment: {str(err)}", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}", parent=self.root)

    def fetch_all_payments(self):
        conn = mysql.connector.connect(host="localhost", username="root", password="11223344", database="hotel")
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT payment_id, booking_ref, payment_amount, payment_date, payment_method FROM payment ORDER BY payment_date DESC")
        rows = my_cursor.fetchall()

        self.payment_table.delete(*self.payment_table.get_children())
        for i in rows:
            self.payment_table.insert("", END, values=i)
        conn.close()

    def get_cursor(self, event=""):
        cursor_row = self.payment_table.focus()
        content = self.payment_table.item(cursor_row)
        row = content["values"]

        self.var_booking_ref.set(row[1])
        self.var_payment_amount.set(row[2])
        self.var_payment_method.set(row[4])
        self.fetch_booking_details() # Re-fetch to update total and due amounts

    def clear_fields(self):
        self.var_booking_ref.set("")
        self.var_payment_amount.set("")
        self.var_payment_method.set("Cash")
        self.var_total_booking_amount.set("0.0")
        self.var_due_amount.set("0.0")
        self.entry_booking_ref.focus_set()


if __name__ == '__main__':
    root = Tk()
    obj = PaymentWindow(root)
    root.mainloop()