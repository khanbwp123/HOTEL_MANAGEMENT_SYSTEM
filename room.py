# room.py
from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
from datetime import datetime, date
import random
import mysql.connector

# --- IMPORTANT: Configure your MySQL credentials here ---
# Using 'root' as requested. Replace 'your_root_password' with your actual root password.
DB_CONFIG = {
    "host": "localhost",
    "username": "root",
    "password": "11223344", # Assuming this is your root password based on previous context
    "database": "hotel"
}
# --------------------------------------------------------

class Roombooking:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("1295x550+230+220")
        self.root.minsize(800, 500)
        self.root.resizable(True, True)

        #=======variables========#
        self.var_Ref = StringVar()
        x = random.randint(10000, 99999)
        self.var_Ref.set(str(x))

        self.var_contact = StringVar()
        self.var_checkin = StringVar()
        self.var_checkout = StringVar()
        self.var_roomtype = StringVar()
        self.var_roomavailable = StringVar()
        self.var_meal = StringVar()
        self.var_noofdays = StringVar()
        self.var_paidtax = StringVar(value="0.0")
        self.var_actualtotal = StringVar(value="0.0")
        self.var_total = StringVar(value="0.0")
        self.var_total_amount = StringVar(value="0.0")
        self.var_booking_status = StringVar(value="Pending")

        # =======title========
        lbl_title = Label(self.root, text="ROOM BOOKING DETAILS", font=("times new roman", 18, "bold"), bg="black",
                          fg="gold", bd=4, relief=RIDGE)
        lbl_title.place(x=0, y=0, width=1295, height=50)

        # ======LOGO==========
        # Ensure this path is correct:
        img2 = Image.open(r"C:\Users\SAEEDCOMPUTERS\Downloads\img2.png")
        img2 = img2.resize((100, 40), Image.Resampling.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)

        lblimg = Label(self.root, image=self.photoimg2, bd=0, relief=RIDGE)
        lblimg.place(x=5, y=2, width=100, height=40)

        # ========LABELFRAME======
        labelframeleft = LabelFrame(self.root, bd=2, relief=RIDGE, text="Roombooking Details", font=("arial", 12, "bold"),
                                    padx=2)
        labelframeleft.place(x=5, y=50, width=425, height=530)

        # Booking Reference (Ref)
        lbl_ref = Label(labelframeleft, text="Booking Ref:", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_ref.grid(row=0, column=0, sticky=W)
        enty_ref = ttk.Entry(labelframeleft, textvariable=self.var_Ref, width=20, font=("arial", 13, "bold"), state="readonly")
        enty_ref.grid(row=0, column=1, sticky=W)

        # Customer Contact (row 1 now)
        lbl_cust_contact = Label(labelframeleft, text="Customer Contact:", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_cust_contact.grid(row=1, column=0, sticky=W)

        enty_contact = ttk.Entry(labelframeleft,textvariable=self.var_contact,width=20,font=("arial", 13, "bold"))
        enty_contact.grid(row=1, column=1,sticky=W)

        #FETCH DATA BUTTON (adjusted y-position)
        btn_Fetch = Button(labelframeleft,command=self.Fetch_contact,text="FETCH",font=("arial", 11, "bold"), bg="black",fg="gold", width=8)
        btn_Fetch.place(x=346,y=44)

        # Customer_check in date(row 2)
        check_in_date = Label(labelframeleft, text="Checkin Date:", font=("arial", 12, "bold"), padx=2, pady=6)
        check_in_date.grid(row=2, column=0, sticky=W)

        txtcheck_in_date= ttk.Entry(labelframeleft,textvariable=self.var_checkin,  width=29, font=("arial", 13, "bold"))
        txtcheck_in_date.grid(row=2, column=1)

        # Customer_check out date(row 3)
        check_out_date = Label(labelframeleft, text="Checkout Date:", font=("arial", 12, "bold"), padx=2, pady=6)
        check_out_date.grid(row=3, column=0, sticky=W)

        txtcheck_out_date = ttk.Entry(labelframeleft,textvariable=self.var_checkout, width=29, font=("arial", 13, "bold"))
        txtcheck_out_date.grid(row=3, column=1)

        # ======ROOM TYPE ===== (row 4)
        label_RoomType = Label(labelframeleft, text="Room type:", font=("arial", 12, "bold"), padx=2, pady=6)
        label_RoomType.grid(row=4, column=0, sticky=W)

        # Hardcoded Room Types + Try to fetch from DB
        hardcoded_room_types = ["Single", "Double", "Luxury", "Duplex"]
        room_types = []
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT DISTINCT roomtype FROM details")
            db_room_types = [item[0] for item in my_cursor.fetchall()]
            conn.close()
            # Combine unique hardcoded and DB fetched room types
            room_types = sorted(list(set(hardcoded_room_types + db_room_types)))
        except mysql.connector.Error as err:
            messagebox.showwarning("DB Warning", f"Could not fetch room types from database: {err}\nUsing hardcoded values.", parent=self.root)
            room_types = hardcoded_room_types
        except Exception as e:
            messagebox.showwarning("Warning", f"An unexpected error occurred while fetching room types: {str(e)}\nUsing hardcoded values.", parent=self.root)
            room_types = hardcoded_room_types

        self.combo_RoomType = ttk.Combobox(labelframeleft, textvariable=self.var_roomtype, font=("arial", 12, "bold"),
                                           width=27, state="readonly")
        self.combo_RoomType["value"] = room_types
        if room_types:
            self.combo_RoomType.set(room_types[0]) # Set default to first item if available
        self.combo_RoomType.grid(row=4, column=1)

        #available room (row 5)
        lblRoomAvailable = Label(labelframeleft, text="Available Room:", font=("arial", 12, "bold"), padx=2, pady=6)
        lblRoomAvailable.grid(row=5, column=0, sticky=W)

        # Populate Available Room Combobox
        # This will ONLY fetch from the database, as room numbers are dynamic
        available_rooms = []
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT roomno FROM details WHERE availability_status = 'Available'")
            available_rooms = [item[0] for item in my_cursor.fetchall()]
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("DB Error", f"Failed to fetch available rooms: {err}\nEnsure MySQL server is running and credentials are correct, and 'details' table has data.", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}", parent=self.root)

        self.combo_roomno = ttk.Combobox(labelframeleft, textvariable=self.var_roomavailable,
                                         font=("arial", 12, "bold"), width=27, state="readonly")
        self.combo_roomno["value"] = available_rooms
        if available_rooms:
            self.combo_roomno.set(available_rooms[0]) # Set default to first item if available
        self.combo_roomno.grid(row=5, column=1)


        #MEAL (row 6)
        lblMeal = Label(labelframeleft, text="Meal:", font=("arial", 12, "bold"), padx=2, pady=6)
        lblMeal.grid(row=6, column=0, sticky=W)
        combo_meal = ttk.Combobox(labelframeleft, textvariable=self.var_meal, width=27, font=("arial", 13, "bold"), state="readonly")
        combo_meal["values"] = ("None", "Breakfast", "Lunch", "Dinner")
        combo_meal.current(0)
        combo_meal.grid(row=6, column=1)

        #number of days===== (row 7)
        lblNoOfDays = Label(labelframeleft, text="No. of Days:", font=("arial", 12, "bold"), padx=2, pady=6)
        lblNoOfDays.grid(row=7, column=0, sticky=W)
        txtNoOfDays= ttk.Entry(labelframeleft,textvariable=self.var_noofdays, width=29, font=("arial", 13, "bold"))
        txtNoOfDays.grid(row=7, column=1)

        #PAID TAX (row 8) - Calculated, so readonly
        lblPaidTax = Label(labelframeleft, text="Paid Taxes:", font=("arial", 12, "bold"), padx=2, pady=6)
        lblPaidTax.grid(row=8, column=0, sticky=W)
        txtPaidTax = ttk.Entry(labelframeleft,textvariable=self.var_paidtax, width=29, font=("arial", 13, "bold"), state="readonly")
        txtPaidTax.grid(row=8, column=1)

        #SUB TOTAL===== (row 9) - Calculated, so readonly
        lblSubTotal = Label(labelframeleft, text="Sub Total:",font=("arial",12,"bold"),padx=2,pady=6)
        lblSubTotal.grid(row=9, column=0, sticky=W)
        txtSubTotal = ttk.Entry(labelframeleft,textvariable=self.var_actualtotal,width=29, font=("arial", 13, "bold"), state="readonly")
        txtSubTotal.grid(row=9, column=1)

        #TOTAL COST==== (row 10) - Calculated, so readonly
        lblTotalCost = Label(labelframeleft, text="Total Cost:", font=("arial", 12, "bold"), padx=2, pady=6)
        lblTotalCost.grid(row=10, column=0, sticky=W)
        txtTotalCost = ttk.Entry(labelframeleft,textvariable=self.var_total_amount, width=29, font=("arial", 13, "bold"), state="readonly")
        txtTotalCost.grid(row=10, column=1)

        # BOOKING STATUS (row 11) - Readonly
        lblBookingStatus = Label(labelframeleft, text="Booking Status:", font=("arial", 12, "bold"), padx=2, pady=6)
        lblBookingStatus.grid(row=11, column=0, sticky=W)
        entyBookingStatus = ttk.Entry(labelframeleft, textvariable=self.var_booking_status, width=29, font=("arial", 13, "bold"), state="readonly")
        entyBookingStatus.grid(row=11, column=1)


        #BILL BUTTON ===== (adjusted row)
        btn_Bill=Button(labelframeleft, text="BILL",command=self.total, font=("arial", 11, "bold"), bg="black", fg="gold", width=10)
        btn_Bill.grid(row=12, column=0, padx=1,sticky=W, pady=5)

        # BUTTON frame
        btn_frame = Frame(labelframeleft, bd=2, relief=RIDGE)
        btn_frame.place(x=0, y=470, width=412, height=40)

        btn_Add = Button(btn_frame, text="Add",command=self.add_data,font=("arial", 11, "bold"), bg="black",fg="gold", width=10)
        btn_Add.grid(row=0, column=0, padx=1)

        btn_Update = Button(btn_frame, text="UPDATE",command=self.update,font=("arial", 11, "bold"), bg="black",fg="gold", width=10)
        btn_Update.grid(row=0, column=1, padx=1)

        btn_Delete = Button(btn_frame, text="DELETE",command=self.mDelete,font=("arial", 11, "bold"), bg="black",fg="gold", width=10)
        btn_Delete.grid(row=0, column=2, padx=1)

        btn_Reset = Button(btn_frame, text="RESET",command=self.reset,font=("arial", 11, "bold"), bg="black",fg="gold", width=9)
        btn_Reset.grid(row=0, column=3, padx=1)


        #RIGHT SIDE IMAGE =====
        # Ensure this path is correct:
        img0 = Image.open(r"C:\Users\SAEEDCOMPUTERS\Downloads\BED.jpg")
        img0 = img0.resize((520,200), Image.Resampling.LANCZOS)
        self.photoimg0 = ImageTk.PhotoImage(img0)

        lblimg_right = Label(self.root,image=self.photoimg0, bd=0, relief=RIDGE)
        lblimg_right.place(x=760, y=55, width=520, height=200)

        # table frame search sys
        Table_Frame = LabelFrame(self.root, bd=2, relief=RIDGE, text="VIEW DETAILS AND SEARCH SYSTEM",
                                 font=("arial", 12, "bold"), padx=2)
        Table_Frame.place(x=435, y=265, width=860, height=275)

        lblSearchBy = Label(Table_Frame, font=("arial", 12, "bold"), text="SEARCH BY", bg="red", fg="white")
        lblSearchBy.grid(row=0, column=0, sticky=W, padx=2)

        self.search_var = StringVar()
        combo_Search = ttk.Combobox(Table_Frame, textvariable=self.search_var, font=("arial", 12, "bold"), width=24,
                                    state="readonly")
        combo_Search["value"] = ("Contact.", "Room No.", "Booking Ref")
        combo_Search.grid(row=0, column=1, padx=2)

        self.txt_search = StringVar()
        txtSearch = ttk.Entry(Table_Frame, textvariable=self.txt_search, width=24, font=("arial", 13, "bold"))
        txtSearch.grid(row=0, column=2, padx=2)

        btn_Search = Button(Table_Frame, text="SEARCH",command=self.search, font=("arial", 12, "bold"),bg="black",
                            fg="gold", width=10)
        btn_Search.grid(row=0, column=3, padx=1)

        btn_ShowAll = Button(Table_Frame, text="Show All",command=self.fetch_data, font=("arial", 12, "bold"),
                             bg="black", fg="gold", width=10)
        btn_ShowAll.grid(row=0, column=4, padx=1)

        # =======SHOW DATA TABLE=====
        details_table = Frame(Table_Frame, bd=2, relief=RIDGE)
        details_table.place(x=0, y=50, width=860, height=200)

        scroll_x = ttk.Scrollbar(details_table, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(details_table, orient=VERTICAL)

        self.room_table = ttk.Treeview(details_table,column=("Ref", "contact","checkin","checkout","roomtype","roomavailable","meal","noofdays", "TotalAmount", "BookingStatus"),xscrollcommand=scroll_x.set
        ,yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.room_table.xview)
        scroll_y.config(command=self.room_table.yview)

        self.room_table.heading("Ref", text="Ref No.")
        self.room_table.heading("contact", text="Contact")
        self.room_table.heading("checkin", text="Check-in")
        self.room_table.heading("checkout", text="Check-out")
        self.room_table.heading("roomtype", text="Room Type")
        self.room_table.heading("roomavailable", text="Room No.")
        self.room_table.heading("meal",text="Meal")
        self.room_table.heading("noofdays", text="No. Of Days")
        self.room_table.heading("TotalAmount", text="Total Amt.")
        self.room_table.heading("BookingStatus", text="Status")


        self.room_table["show"] = "headings"

        self.room_table.column("Ref", width=80)
        self.room_table.column("contact", width=100)
        self.room_table.column("checkin", width=100)
        self.room_table.column("checkout", width=100)
        self.room_table.column("roomtype", width=100)
        self.room_table.column("roomavailable", width=100)
        self.room_table.column("meal", width=80)
        self.room_table.column("noofdays", width=80)
        self.room_table.column("TotalAmount", width=100)
        self.room_table.column("BookingStatus", width=100)

        self.room_table.pack(fill=BOTH, expand=1)
        self.room_table.bind("<ButtonRelease-1>",self.get_cursor)
        self.fetch_data()

        # --- Initialize showDataframe and its labels here ---
        self.showDataframe=Frame(self.root,bd=4,relief=RIDGE,padx=2)
        self.showDataframe.place(x=455,y=55,width=300,height=180)

        # Create labels initially, set text to empty or placeholders
        self.lbl_name_value = Label(self.showDataframe, text="", font=("arial", 12, "bold"))
        self.lbl_name_value.place(x=90, y=0)
        self.lbl_gender_value = Label(self.showDataframe, text="", font=("arial", 12, "bold"))
        self.lbl_gender_value.place(x=90, y=30)
        self.lbl_email_value = Label(self.showDataframe, text="", font=("arial", 12, "bold"))
        self.lbl_email_value.place(x=90, y=60)
        self.lbl_nationality_value = Label(self.showDataframe, text="", font=("arial", 12, "bold"))
        self.lbl_nationality_value.place(x=90, y=90)
        self.lbl_address_value = Label(self.showDataframe, text="", font=("arial", 12, "bold"))
        self.lbl_address_value.place(x=90,y=120)

        # Also place the static labels
        Label(self.showDataframe,text="Name:",font=("arial",12,"bold")).place(x=0,y=0)
        Label(self.showDataframe, text="Gender:", font=("arial", 12, "bold")).place(x=0, y=30)
        Label(self.showDataframe, text="Email:", font=("arial", 12, "bold")).place(x=0, y=60)
        Label(self.showDataframe, text="Nationality:", font=("arial", 12, "bold")).place(x=0, y=90)
        Label(self.showDataframe, text="Address:", font=("arial", 12, "bold")).place(x=0, y=120)


    def total(self):
        # These are hardcoded prices, adjust as needed or fetch from DB if available
        room_prices = {"Single": 1000, "Double": 1500, "Luxury": 2500, "Duplex": 3500}
        meal_prices = {"Breakfast": 300, "Lunch": 500, "Dinner": 700, "None": 0, "": 0} # Added "" for default

        room_cost = room_prices.get(self.var_roomtype.get(), 0)
        meal_cost = meal_prices.get(self.var_meal.get(), 0)

        try:
            checkin_date = datetime.strptime(self.var_checkin.get(), "%d/%m/%Y").date()
            checkout_date = datetime.strptime(self.var_checkout.get(), "%d/%m/%Y").date()
            num_days = (checkout_date - checkin_date).days
            if num_days <= 0: # Ensure at least 1 day for calculation
                num_days = 1
            self.var_noofdays.set(str(num_days))
        except ValueError:
            # If date format is wrong, try to get days directly if available or default to 1
            try:
                num_days = int(self.var_noofdays.get() or 1)
            except ValueError:
                num_days = 1 # Default to 1 day if input is invalid

        sub_total = (room_cost * num_days) + (meal_cost * num_days)
        tax = sub_total * 0.10 # 10% tax
        final_total = sub_total + tax

        self.var_actualtotal.set(f"{sub_total:.2f}")
        self.var_paidtax.set(f"{tax:.2f}")
        self.var_total_amount.set(f"{final_total:.2f}")
        self.var_total.set(f"{final_total:.2f}") # This might be redundant if var_total_amount is used for display

        return final_total


    def add_data(self):
        if (self.var_contact.get() == "" or self.var_checkin.get() == "" or
            self.var_checkout.get() == "" or self.var_roomtype.get() == "" or
            self.var_roomavailable.get() == ""):
            messagebox.showerror("ERROR", "All primary booking fields (Contact, Checkin/out, Room Type, Room No.) are required!", parent=self.root)
            return

        try:
            calculated_total = self.total()
            if not calculated_total:
                messagebox.showerror("Error", "Could not calculate total amount. Please ensure dates/room type are valid.", parent=self.root)
                return
        except Exception as e:
            messagebox.showerror("Calculation Error", f"Error calculating total: {str(e)}", parent=self.root)
            return

        conn = None
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            my_cursor = conn.cursor()

            # First, check if the room is indeed available before booking
            my_cursor.execute("SELECT availability_status FROM details WHERE roomno = %s", (self.var_roomavailable.get(),))
            room_status = my_cursor.fetchone()
            if room_status and room_status[0] == 'Booked':
                messagebox.showerror("Error", f"Room {self.var_roomavailable.get()} is already booked. Please choose another.", parent=self.root)
                conn.close()
                return

            # Update the details table to 'Booked'
            my_cursor.execute("UPDATE details SET availability_status = 'Booked' WHERE roomno = %s", (self.var_roomavailable.get(),))

            my_cursor.execute(
                "INSERT INTO room (Ref, contact, checkin, checkout, roomtype, roomavailable, meal, noofdays, TotalAmount, BookingStatus) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    self.var_Ref.get(),
                    self.var_contact.get(),
                    self.var_checkin.get(),
                    self.var_checkout.get(),
                    self.var_roomtype.get(),
                    self.var_roomavailable.get(),
                    self.var_meal.get(),
                    self.var_noofdays.get(),
                    float(self.var_total_amount.get()),
                    self.var_booking_status.get(),
                )
            )
            conn.commit()
            conn.close()
            self.fetch_data()
            messagebox.showinfo("Success", "Room booking added successfully!", parent=self.root)
            self.reset()
            self.update_available_rooms_dropdown() # Refresh available rooms

        except mysql.connector.Error as err:
            if err.errno == 1062: # Duplicate entry for primary key (Ref)
                messagebox.showerror("Error", "Booking Reference already exists. Please try again or use a different reference.", parent=self.root)
            else:
                messagebox.showerror("DB Error", f"Failed to add booking: {err}", parent=self.root)
        except Exception as es:
            messagebox.showwarning("Warning", f"Something went wrong: {str(es)}", parent=self.root)


    def get_cursor(self, event=""):
        cursor_row = self.room_table.focus()
        content = self.room_table.item(cursor_row)
        row = content["values"]

        if not row:
            self.reset()
            return

        self.var_Ref.set(row[0])
        self.var_contact.set(row[1])
        self.var_checkin.set(row[2])
        self.var_checkout.set(row[3])
        self.var_roomtype.set(row[4])
        self.var_roomavailable.set(row[5])
        self.var_meal.set(row[6])
        self.var_noofdays.set(row[7])
        self.var_total_amount.set(row[8])
        self.var_booking_status.set(row[9])

        final_total = float(row[8])
        # Assuming 10% tax. If total = sub_total * 1.1, then sub_total = total / 1.1
        sub_total = final_total / 1.1
        tax = final_total - sub_total
        self.var_actualtotal.set(f"{sub_total:.2f}")
        self.var_paidtax.set(f"{tax:.2f}")


    def update(self):
        if self.var_Ref.get() == "":
            messagebox.showerror("Error", "Booking Reference is required for update.", parent=self.root)
            return

        # Recalculate total if any related fields might have changed
        try:
            self.total()
        except Exception as e:
            messagebox.showerror("Calculation Error", f"Error recalculating total for update: {str(e)}",
                                 parent=self.root)
            return

        conn = None
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            my_cursor = conn.cursor()

            # Get old room number to revert its status if room number changed
            my_cursor.execute("SELECT roomavailable FROM room WHERE Ref = %s", (self.var_Ref.get(),))
            old_room_available_row = my_cursor.fetchone()
            old_room_available = old_room_available_row[0] if old_room_available_row else None

            # Check if the new room (if changed) is available
            if old_room_available and old_room_available != self.var_roomavailable.get():
                my_cursor.execute("SELECT availability_status FROM details WHERE roomno = %s", (self.var_roomavailable.get(),))
                new_room_status = my_cursor.fetchone()
                if new_room_status and new_room_status[0] == 'Booked':
                    messagebox.showerror("Error", f"New room {self.var_roomavailable.get()} is already booked. Please choose another.", parent=self.root)
                    conn.close()
                    return


            my_cursor.execute(
                "UPDATE room SET contact=%s, checkin=%s, checkout=%s, roomtype=%s, roomavailable=%s, meal=%s, noofdays=%s, TotalAmount=%s, BookingStatus=%s WHERE Ref=%s",
                (
                    self.var_contact.get(),
                    self.var_checkin.get(),
                    self.var_checkout.get(),
                    self.var_roomtype.get(),
                    self.var_roomavailable.get(),
                    self.var_meal.get(),
                    self.var_noofdays.get(),
                    float(self.var_total_amount.get()),
                    self.var_booking_status.get(),
                    self.var_Ref.get(),
                )
            )
            conn.commit()

            # Update room availability status in 'details' table
            # If room number changed, make the old room available and new room booked
            if old_room_available and old_room_available != self.var_roomavailable.get():
                my_cursor.execute("UPDATE details SET availability_status = 'Available' WHERE roomno = %s", (old_room_available,))
                conn.commit()

            my_cursor.execute("UPDATE details SET availability_status = 'Booked' WHERE roomno = %s", (self.var_roomavailable.get(),))
            conn.commit()


            conn.close()
            self.fetch_data()
            messagebox.showinfo("Update", "Room booking updated successfully!", parent=self.root)
            self.reset()
            self.update_available_rooms_dropdown() # Refresh dropdown after update

        except mysql.connector.Error as err:
            messagebox.showerror("DB Error", f"Failed to update booking: {err}", parent=self.root)
        except Exception as es:
            messagebox.showwarning("Warning", f"Something went wrong: {str(es)}", parent=self.root)

    def mDelete(self):
        mDelete = messagebox.askyesno("Hotel Management System", "Do you want to delete this room booking?", parent=self.root)
        if mDelete:
            conn = None
            try:
                conn = mysql.connector.connect(**DB_CONFIG)
                my_cursor = conn.cursor()

                # Get the room number before deleting the booking to update its status
                my_cursor.execute("SELECT roomavailable FROM room WHERE Ref=%s", (self.var_Ref.get(),))
                room_no_to_free = my_cursor.fetchone()
                if room_no_to_free:
                    room_no_to_free = room_no_to_free[0]
                    # Update details table: set room to 'Available'
                    my_cursor.execute("UPDATE details SET availability_status = 'Available' WHERE roomno = %s", (room_no_to_free,))
                    conn.commit()

                query = "DELETE FROM room WHERE Ref=%s"
                values = (self.var_Ref.get(),)
                my_cursor.execute(query, values)
                conn.commit()
                conn.close()
                self.fetch_data()
                messagebox.showinfo("Deleted", "Room booking deleted successfully", parent=self.root)
                self.reset()
                self.update_available_rooms_dropdown() # Refresh dropdown after deletion
            except mysql.connector.Error as err:
                messagebox.showerror("DB Error", f"Failed to delete booking: {err}", parent=self.root)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete: {str(e)}", parent=self.root)
        else:
            return

    def reset(self):
        self.var_Ref.set(str(random.randint(10000, 99999)))
        self.var_contact.set("")
        self.var_checkin.set("")
        self.var_checkout.set("")
        self.var_roomtype.set("") # Reset room type selection
        self.var_roomavailable.set("") # Reset available room selection
        self.var_meal.set("None")
        self.var_noofdays.set("")
        self.var_paidtax.set("0.0")
        self.var_actualtotal.set("0.0")
        self.var_total.set("0.0")
        self.var_total_amount.set("0.0")
        self.var_booking_status.set("Pending")

        self.lbl_name_value.config(text="")
        self.lbl_gender_value.config(text="")
        self.lbl_email_value.config(text="")
        self.lbl_nationality_value.config(text="")
        self.lbl_address_value.config(text="")

        # Re-populate dropdowns to reflect current state (e.g., if a room was freed up)
        self.update_available_rooms_dropdown()
        # No need to update room types here unless you expect them to change dynamically


    def fetch_data(self):
        conn = None
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT Ref, contact, checkin, checkout, roomtype, roomavailable, meal, noofdays, TotalAmount, BookingStatus FROM room")
            rows = my_cursor.fetchall()
            if len(rows) != 0:
                self.room_table.delete(*self.room_table.get_children())
                for i in rows:
                    self.room_table.insert("", END, values=i)
            else:
                self.room_table.delete(*self.room_table.get_children())
        except mysql.connector.Error as err:
            messagebox.showerror("DB Error", f"Failed to fetch data: {err}", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}", parent=self.root)
        finally:
            if conn:
                conn.close()


    def Fetch_contact(self):
        if not self.var_contact.get():
           messagebox.showerror("Error","Please Enter the contact number",parent=self.root)
           return

        conn = None
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            my_cursor = conn.cursor()
            query=("select Name, Gender, Email, Nationality, Address from customer where Mobile=%s")
            value=(self.var_contact.get(),)
            my_cursor.execute(query,value)
            row=my_cursor.fetchone()

            if row is None:
                messagebox.showerror("Error","This customer contact number not found",parent=self.root)
                self.lbl_name_value.config(text="")
                self.lbl_gender_value.config(text="")
                self.lbl_email_value.config(text="")
                self.lbl_nationality_value.config(text="")
                self.lbl_address_value.config(text="")
            else:
                self.lbl_name_value.config(text=row[0])
                self.lbl_gender_value.config(text=row[1])
                self.lbl_email_value.config(text=row[2])
                self.lbl_nationality_value.config(text=row[3])
                self.lbl_address_value.config(text=row[4])

        except mysql.connector.Error as err:
            messagebox.showerror("DB Error", f"Failed to fetch contact data: {err}", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}", parent=self.root)
        finally:
            if conn:
                conn.close()


    def search(self):
        conn = None
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            my_cursor = conn.cursor()

            search_by = self.search_var.get()
            if search_by == "Room No.":
                column_name = "roomavailable"
            elif search_by == "Contact.":
                column_name = "contact"
            elif search_by == "Booking Ref":
                column_name = "Ref"
            else:
                messagebox.showerror("Error", "Invalid search criteria", parent=self.root)
                return

            query = f"SELECT Ref, contact, checkin, checkout, roomtype, roomavailable, meal, noofdays, TotalAmount, BookingStatus FROM room WHERE {column_name} LIKE %s"
            value = ("%" + self.txt_search.get() + "%",)
            my_cursor.execute(query, value)

            rows = my_cursor.fetchall()
            if rows:
                self.room_table.delete(*self.room_table.get_children())
                for row in rows:
                    self.room_table.insert("", END, values=row)
            else:
                messagebox.showinfo("Not Found", "No matching records found", parent=self.root)

        except mysql.connector.Error as err:
            messagebox.showerror("DB Error", f"Failed to search: {err}", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}", parent=self.root)
        finally:
            if conn:
                conn.close()

    def update_available_rooms_dropdown(self):
        # This function re-fetches available rooms and updates the dropdown
        available_rooms = []
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT roomno FROM details WHERE availability_status = 'Available'")
            available_rooms = [item[0] for item in my_cursor.fetchall()]
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("DB Error", f"Failed to refresh available rooms: {err}", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}", parent=self.root)

        try:
            self.combo_roomno["value"] = available_rooms
            self.var_roomavailable.set("") # Clear current selection
            if available_rooms:
                self.combo_roomno.set(available_rooms[0]) # Set default if rooms exist
        except AttributeError:
            print("Combobox for room numbers not yet assigned as instance attribute. Skipping update.")


if __name__ == '__main__':
    root = Tk()
    obj = Roombooking(root)
    root.mainloop()