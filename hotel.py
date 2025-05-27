# hotel.py
from tkinter import *
from PIL import Image, ImageTk
from customer import Cust_Win
from room import Roombooking
from details import Details_Room
from staff import Staff_Win
from service import Service_Win
from feedback import Feedback_Win
from payment import PaymentWindow # <--- Ensure this is imported
from inventory import Inventory_Win
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime, date

# --- New: Function to handle report table creation ---
def setup_report_table():
    try:
        conn = mysql.connector.connect(host="localhost", username="root", password="11223344", database="hotel")
        my_cursor = conn.cursor()
        # Create reports table if it doesn't exist
        my_cursor.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                report_id INT AUTO_INCREMENT PRIMARY KEY,
                report_type VARCHAR(50) NOT NULL,
                report_date DATE,
                generation_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                generated_by VARCHAR(100)
            )
        """)
        conn.commit()
        conn.close()
        # messagebox.showinfo("DB Setup", "Reports table ensured.") # Optional: For debugging
    except Exception as e:
        messagebox.showerror("DB Error", f"Failed to setup reports table: {str(e)}")

# --- Call the setup function when the application starts or module is loaded ---
setup_report_table()


# --- New: Function to handle staff table creation ---
def setup_staff_table():
    try:
        conn = mysql.connector.connect(host="localhost", username="root", password="11223344", database="hotel")
        my_cursor = conn.cursor()
        # Create staff table if it doesn't exist
        my_cursor.execute("""
            CREATE TABLE IF NOT EXISTS staff (
                staff_id VARCHAR(10) PRIMARY KEY,
                staff_name VARCHAR(100) NOT NULL,
                staff_role VARCHAR(50)
            )
        """)
        conn.commit()
        conn.close()
        # messagebox.showinfo("DB Setup", "Staff table ensured.") # Optional: For debugging
    except Exception as e:
        messagebox.showerror("DB Error", f"Failed to setup staff table: {str(e)}")

 # --- New: Function to handle service table creation ---
def setup_service_table():
    try:
        conn = mysql.connector.connect(host="localhost", username="root", password="11223344", database="hotel")
        my_cursor = conn.cursor()
        # Create services table if it doesn't exist
        my_cursor.execute("""
            CREATE TABLE IF NOT EXISTS services (
                service_id VARCHAR(10) PRIMARY KEY,
                service_name VARCHAR(100) NOT NULL,
                service_price DECIMAL(10, 2)
            )
        """)
        conn.commit()
        conn.close()
        # messagebox.showinfo("DB Setup", "Services table ensured.") # Optional: For debugging
    except Exception as e:
        messagebox.showerror("DB Error", f"Failed to setup services table: {str(e)}")

# --- New: Function to handle department table creation ---
def setup_department_table():
    try:
        conn = mysql.connector.connect(host="localhost", username="root", password="11223344", database="hotel")
        my_cursor = conn.cursor()
        # Create departments table if it doesn't exist
        my_cursor.execute("""
            CREATE TABLE IF NOT EXISTS departments (
                department_id INT AUTO_INCREMENT PRIMARY KEY,
                department_name VARCHAR(100) NOT NULL UNIQUE
            )
        """)
        # Optionally, insert some default departments if the table is new and empty
        my_cursor.execute("INSERT IGNORE INTO departments (department_name) VALUES ('Front Desk')")
        my_cursor.execute("INSERT IGNORE INTO departments (department_name) VALUES ('Housekeeping')")
        my_cursor.execute("INSERT IGNORE INTO departments (department_name) VALUES ('Restaurant')")
        my_cursor.execute("INSERT IGNORE INTO departments (department_name) VALUES ('Management')")
        my_cursor.execute("INSERT IGNORE INTO departments (department_name) VALUES ('Security')")
        conn.commit()
        conn.close()
        # messagebox.showinfo("DB Setup", "Departments table ensured.") # Optional: For debugging
    except Exception as e:
        messagebox.showerror("DB Error", f"Failed to setup departments table: {str(e)}")

    # --- New: Function to handle guest_feedback table creation ---
# --- New: Function to handle guest_feedback table creation ---
def setup_feedback_table():
    try:
        conn = mysql.connector.connect(host="localhost", username="root", password="11223344", database="hotel")
        my_cursor = conn.cursor()
        # Create guest_feedback table if it doesn't exist
        my_cursor.execute("""
            CREATE TABLE IF NOT EXISTS guest_feedback (
                feedback_id VARCHAR(10) PRIMARY KEY,
                booking_id VARCHAR(100),
                guest_contact VARCHAR(20), -- REMOVED NOT NULL
                feedback_type VARCHAR(50),
                comments TEXT NOT NULL,
                feedback_date DATE,
                resolution_status VARCHAR(50),
                FOREIGN KEY (guest_contact) REFERENCES customer(Mobile) ON DELETE SET NULL ON UPDATE CASCADE
            )
        """)
        conn.commit()
        conn.close()
    except Exception as e:
        messagebox.showerror("DB Error", f"Failed to setup guest_feedback table: {str(e)}")

# --- New: Function to handle inventory table creation ---
def setup_inventory_table():
    try:
        conn = mysql.connector.connect(host="localhost", username="root", password="11223344", database="hotel")
        my_cursor = conn.cursor()
        # Create inventory table if it doesn't exist
        my_cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                item_id VARCHAR(10) PRIMARY KEY,
                item_name VARCHAR(100) NOT NULL,
                category VARCHAR(50),
                quantity_on_hand INT DEFAULT 0,
                unit_of_measure VARCHAR(20),
                reorder_level INT DEFAULT 0,
                last_restocked_date DATE,
                supplier_id VARCHAR(10) -- For now, just a string; can become FK to Supplier later
            )
        """)
        conn.commit()
        conn.close()
        # messagebox.showinfo("DB Setup", "Inventory table ensured.") # Optional: For debugging
    except Exception as e:
        messagebox.showerror("DB Error", f"Failed to setup inventory table: {str(e)}")


 # <-- Call the new inventory setup function here

def setup_service_table():
    try:
        conn = mysql.connector.connect(host="localhost", username="root", password="11223344", database="hotel")
        my_cursor = conn.cursor()
        # Create services table if it doesn't exist
        my_cursor.execute("""
            CREATE TABLE IF NOT EXISTS services (
                service_id VARCHAR(10) PRIMARY KEY,
                service_name VARCHAR(100) NOT NULL,
                service_price DECIMAL(10, 2)
            )
        """)
        conn.commit()
        conn.close()
    except Exception as e:
        messagebox.showerror("DB Error", f"Failed to setup services table: {str(e)}")

# --- NEW: Function to handle customer table creation with UNIQUE Mobile ---
def setup_customer_table():
    try:
        conn = mysql.connector.connect(host="localhost", username="root", password="11223344", database="hotel")
        my_cursor = conn.cursor()
        my_cursor.execute("""
            CREATE TABLE IF NOT EXISTS customer (
                Ref VARCHAR(20) PRIMARY KEY,
                Name VARCHAR(100),
                Mother VARCHAR(100),
                Gender VARCHAR(10),
                Post VARCHAR(20),
                Mobile VARCHAR(20) UNIQUE, -- THIS IS THE CRUCIAL CHANGE
                Email VARCHAR(100),
                Nationality VARCHAR(50),
                ID_Proof VARCHAR(50),
                ID_No VARCHAR(50),
                Address VARCHAR(255)
            )
        """)
        conn.commit()
        conn.close()
    except Exception as e:
        messagebox.showerror("DB Error", f"Failed to setup customer table: {str(e)}")

def setup_room_table():
    try:
        conn = mysql.connector.connect(host="localhost", username="root", password="11223344", database="hotel")
        my_cursor = conn.cursor()
        # Create room table if it doesn't exist
        # IMPORTANT: Adding TotalAmount and BookingStatus columns
        my_cursor.execute("""
            CREATE TABLE IF NOT EXISTS room (
                Ref VARCHAR(20) PRIMARY KEY, -- Assuming Ref is the unique booking identifier
                contact VARCHAR(20),
                checkin VARCHAR(20),
                checkout VARCHAR(20),
                roomtype VARCHAR(20),
                roomavailable VARCHAR(20), -- This is Room_No
                meal VARCHAR(20),
                noofdays VARCHAR(20),
                TotalAmount DECIMAL(10, 2) DEFAULT 0.00, -- NEW COLUMN
                BookingStatus VARCHAR(50) DEFAULT 'Pending', -- NEW COLUMN
                FOREIGN KEY (contact) REFERENCES customer(Mobile) ON DELETE SET NULL ON UPDATE CASCADE,
                FOREIGN KEY (roomavailable) REFERENCES details(roomno) ON DELETE SET NULL ON UPDATE CASCADE
            )
        """)
        conn.commit()
        conn.close()
        # messagebox.showinfo("DB Setup", "Room table ensured.") # Optional: For debugging
    except Exception as e:
        messagebox.showerror("DB Error", f"Failed to setup room table: {str(e)}")


def setup_details_table():
    try:
        conn = mysql.connector.connect(host="localhost", username="root", password="11223344", database="hotel")
        my_cursor = conn.cursor()
        # Create details table if it doesn't exist
        # IMPORTANT: Adding availability_status column
        my_cursor.execute("""
            CREATE TABLE IF NOT EXISTS details (
                roomno VARCHAR(20) PRIMARY KEY,
                roomtype VARCHAR(50),
                bed VARCHAR(50),
                price VARCHAR(50),
                availability_status VARCHAR(50) DEFAULT 'Available' -- NEW COLUMN
            )
        """)
        conn.commit()
        conn.close()
        # messagebox.showinfo("DB Setup", "Details table ensured.") # Optional: For debugging
    except Exception as e:
        messagebox.showerror("DB Error", f"Failed to setup details table: {str(e)}")

def setup_payment_table():
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="11223344", database="hotel")
            my_cursor = conn.cursor()
            my_cursor.execute("""
                CREATE TABLE IF NOT EXISTS payment (
                    payment_id INT AUTO_INCREMENT PRIMARY KEY,
                    booking_ref VARCHAR(20) NOT NULL,
                    payment_amount DECIMAL(10, 2) NOT NULL,
                    payment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    payment_method VARCHAR(50),
                    FOREIGN KEY (booking_ref) REFERENCES room(Ref) ON DELETE CASCADE ON UPDATE CASCADE
                )
            """)
            conn.commit()
            conn.close()
            # messagebox.showinfo("DB Setup", "Payment table ensured.") # Optional: For debugging
        except Exception as e:
            messagebox.showerror("DB Error", f"Failed to setup payment table: {str(e)}")

    # ... (rest of your hotel.py) ...


# --- Call the setup function when the application starts or module is loaded ---
setup_report_table()
setup_staff_table()
setup_service_table()
setup_customer_table()
setup_department_table() # <-- Call the new department setup function here
setup_feedback_table()
setup_inventory_table()
setup_payment_table() # <--- Payment table setup call
setup_details_table()
setup_room_table()



class HotelManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("1295x550+0+0")

        self.root.minsize(1024, 768)
        self.root.resizable(True, True)

        img1 = Image.open(r"C:\Users\SAEEDCOMPUTERS\Downloads\img1.png")
        img1 = img1.resize((1550, 140), Image.Resampling.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1) #cite: 1

        lblimg = Label(self.root, image=self.photoimg1, bd=4, relief=RIDGE)
        lblimg.place(x=0, y=0, width=1550, height=140)

        #=========logo========#

        img2 = Image.open(r"C:\Users\SAEEDCOMPUTERS\Downloads\img2.png")
        img2 = img2.resize((230, 140), Image.Resampling.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2) #cite: 2

        lbllogo = Label(self.root, image=self.photoimg2, bd=4, relief=RIDGE)
        lbllogo.place(x=0, y=0, width=230, height=140)

        # =======title========
        lbl_title = Label(self.root, text=" PC HOTEL MANAGEMENT SYSTEM", font=("times new roman", 40, "bold"),
                          bg="black", fg="gold", bd=4, relief=RIDGE) #cite: 3
        lbl_title.place(x=0, y=140, width=1550, height=50) #cite: 3

        #======main frame=====
        main_frame = Frame(self.root, bd=4, relief=RIDGE)
        main_frame.place(x=0, y=190, width=1550, height=620)

        # ========== LEFT SIDEBAR SCROLLABLE ==========
        sidebar_frame = Frame(main_frame, bd=4, relief=RIDGE)
        sidebar_frame.place(x=0, y=0, width=230, height=620) #cite: 4

        # Create canvas and scrollbar
        canvas = Canvas(sidebar_frame, width=230, height=620)
        scrollbar = Scrollbar(sidebar_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all") #cite: 5
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ========== MENU TITLE ==========
        lbl_menu = Label(scrollable_frame, text="MENU", font=("times new roman", 20, "bold"),
                         bg="black", fg="gold", bd=4, relief=RIDGE) #cite: 6
        lbl_menu.pack(fill="x") #cite: 6

        # =====btn frame======
        # The btn_frame should be placed inside 'scrollable_frame' if you want it to scroll with content,
        # and then use .pack() or .grid() for its internal buttons.
        # Alternatively, if you want buttons fixed in position, it should be in sidebar_frame and then coordinate adjusted.
        # Given your previous structure, it seems you want the buttons to be part of the fixed sidebar, not necessarily scrollable.
        # If the number of buttons grows very large, then the scrollable_frame approach is better.

        # Let's keep it in main_frame for now and adjust height/Y to fit.
        # This will be simpler than making the button frame scrollable unless strictly necessary.
        btn_frame = Frame(main_frame, bd=4, relief=RIDGE)
        # There are 9 buttons now (0-8). Each button plus pady=1 is approx 30-35 pixels tall.
        # 9 buttons * 35 pixels/button = 315 pixels. Let's make it 320 for some padding.
        # The 'MENU' label in scrollable_frame takes some height. The buttons are inside 'main_frame' relative to it.
        # The sidebar_frame starts at y=0 within main_frame.
        # The MENU label is PACKED into scrollable_frame.
        # The previous btn_frame.place(x=0, y=35...) was correct for its y relative to main_frame.
        # We need to consider its position relative to main_frame if it's its direct child.
        # The sidebar_frame is at x=0, y=0, width=230, height=620 within main_frame.
        # So the btn_frame should be placed within sidebar_frame to appear on the left.

        # Corrected: Place btn_frame inside sidebar_frame
        btn_frame = Frame(sidebar_frame, bd=4, relief=RIDGE)
        # Calculate Y position: lbl_menu is packed at the top of scrollable_frame (which is in canvas, which is in sidebar_frame)
        # The actual y of the buttons needs to account for the lbl_menu and then the padding.
        # Let's try placing btn_frame directly below lbl_menu using pack()
        # To make it work cleanly, btn_frame itself should also be packed into the scrollable_frame.
        # This is the most robust way to handle a variable number of buttons without manually calculating `place` coords.

        # --- Re-architecture for buttons to be properly scrollable ---
        # Instead of placing btn_frame, let's pack buttons directly into scrollable_frame
        # or pack btn_frame into scrollable_frame and then grid buttons into btn_frame.
        # The latter keeps your button grouping.

        btn_frame = Frame(scrollable_frame, bd=4, relief=RIDGE)
        btn_frame.pack(fill="x", pady=5) # Pack the button frame below the MENU label

        cust_btn = Button(btn_frame, text="CUSTOMER", command=self.cust_details, width=22,
                          font=("times new roman", 14, "bold"), bg="black", fg="gold", bd=0, cursor="hand1")
        cust_btn.grid(row=0, column=0, pady=1)

        room_btn = Button(btn_frame, text="ROOM", width=22, command=self.roombooking,
                          font=("times new roman", 14, "bold"), bg="black", fg="gold", bd=0, cursor="hand1")
        room_btn.grid(row=1, column=0, pady=1)

        detail_btn = Button(btn_frame, command=self.detail_room, text="DETAIL", width=22,
                            font=("times new roman", 14, "bold"), bg="black", fg="gold", bd=0, cursor="hand1")
        detail_btn.grid(row=2, column=0, pady=1)

        report_btn = Button(btn_frame, text="REPORT", command=self.open_report_options, width=22,
                            font=("times new roman", 14, "bold"), bg="black", fg="gold", bd=0, cursor="hand1")
        report_btn.grid(row=3, column=0, pady=1)

        staff_btn = Button(btn_frame, text="STAFF", command=self.open_staff_details, width=22,
                           font=("times new roman", 14, "bold"), bg="black", fg="gold", bd=0, cursor="hand1")
        staff_btn.grid(row=4, column=0, pady=1)

        service_btn = Button(btn_frame, text="SERVICE", command=self.open_service_details, width=22,
                             font=("times new roman", 14, "bold"), bg="black", fg="gold", bd=0, cursor="hand1")
        service_btn.grid(row=5, column=0, pady=1)

        feedback_btn = Button(btn_frame, text="FEEDBACK", command=self.open_feedback_details, width=22,
                              font=("times new roman", 14, "bold"), bg="black", fg="gold", bd=0, cursor="hand1")
        feedback_btn.grid(row=6, column=0, pady=1)

        inventory_btn = Button(btn_frame, text="INVENTORY", command=self.open_inventory_details, width=22,
                               font=("times new roman", 14, "bold"), bg="black", fg="gold", bd=0, cursor="hand1")
        inventory_btn.grid(row=7, column=0, pady=1)

        # PAYMENT Button - Now at row 8
        payment_btn = Button(btn_frame, text="PAYMENT", command=self.open_payment_window, width=22,
                             font=("times new roman", 14, "bold"), bg="black", fg="gold", bd=0, cursor="hand1")
        payment_btn.grid(row=8, column=0, pady=1)

        # LOG OUT button is completely removed
        # Increased height
        # ======RIGHT SIDE IMAGE======
        img33 = Image.open(r"C:\Users\SAEEDCOMPUTERS\Downloads\img33.jpg")
        img33 = img33.resize((1310, 590), Image.Resampling.LANCZOS)
        self.photoimg33 = ImageTk.PhotoImage(img33) #cite: 10
        self.lblimg1 = Label(main_frame, image=self.photoimg33, bd=4, relief=RIDGE)
        self.lblimg1.place(x=230, y=0, width=1310, height=590) #cite: 10


    def cust_details(self):
            self.new_window = Toplevel(self.root)
            self.app = Cust_Win(self.new_window)

    def roombooking(self):
        self.new_window = Toplevel(self.root)
        self.app = Roombooking(self.new_window)

    def detail_room(self):
        self.new_window = Toplevel(self.root)
        self.app = Details_Room(self.new_window)

    def open_staff_details(self):
        self.new_window = Toplevel(self.root)
        self.app = Staff_Win(self.new_window)

        # --- NEW: Method to open Service_Win ---
    def open_service_details(self):
            self.new_window = Toplevel(self.root)
            self.app = Service_Win(self.new_window)
        # --- END OF NEW METHOD ---
    def open_feedback_details(self):
        self.new_window = Toplevel(self.root)
        self.app = Feedback_Win(self.new_window)

    def open_inventory_details(self):
        self.new_window = Toplevel(self.root)
        self.app = Inventory_Win(self.new_window)

    def open_payment_window(self):
        self.new_window = Toplevel(self.root)
        self.app = PaymentWindow(self.new_window)

    # --- END OF NEW METHOD ---

    # --- END OF NEW METHOD ---

    # --- NEW: Report Functionality ---
    def open_report_options(self):
        self.report_window = Toplevel(self.root)
        self.report_window.title("Generate Report")
        self.report_window.geometry("500x400+400+250")
        self.report_window.transient(self.root) # Make it modal

        lbl_title = Label(self.report_window, text="SELECT REPORT TYPE", font=("times new roman", 16, "bold"),
                          bg="black", fg="gold", bd=4, relief=RIDGE)
        lbl_title.pack(fill="x", pady=10)

        # Frame for report type selection
        report_type_frame = LabelFrame(self.report_window, bd=2, relief=RIDGE, text="Report Parameters",
                                      font=("arial", 12, "bold"), padx=5, pady=5)
        report_type_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Report Type Selection
        lbl_report_type = Label(report_type_frame, text="Report Type:", font=("arial", 12, "bold"))
        lbl_report_type.grid(row=0, column=0, sticky=W, padx=5, pady=5)

        self.var_report_type = StringVar()
        self.report_type_combo = ttk.Combobox(report_type_frame, textvariable=self.var_report_type,
                                             font=("arial", 12, "bold"), width=25, state="readonly")
        self.report_type_combo["values"] = ("Occupancy Report", "Daily Revenue Report")
        self.report_type_combo.set("Occupancy Report") # Default selection
        self.report_type_combo.grid(row=0, column=1, padx=5, pady=5)
        self.report_type_combo.bind("<<ComboboxSelected>>", self.update_report_ui)


        # Date Selection for Daily Revenue Report (initially hidden)
        self.lbl_report_date = Label(report_type_frame, text="Report Date (DD/MM/YYYY):", font=("arial", 12, "bold"))
        self.lbl_report_date.grid(row=1, column=0, sticky=W, padx=5, pady=5) # Initially visible, but we'll control it

        self.var_report_date = StringVar(value=datetime.now().strftime("%d/%m/%Y")) # Default to today
        self.entry_report_date = ttk.Entry(report_type_frame, textvariable=self.var_report_date,
                                           font=("arial", 12, "bold"), width=27)
        self.entry_report_date.grid(row=1, column=1, padx=5, pady=5)


        # Button to generate report
        btn_generate = Button(self.report_window, text="Generate Report", command=self.generate_selected_report,
                              font=("arial", 12, "bold"), bg="black", fg="gold", width=20)
        btn_generate.pack(pady=10)

        # Area to display report results (using a Treeview for tabular data)
        self.report_results_frame = LabelFrame(self.report_window, bd=2, relief=RIDGE, text="Report Results",
                                               font=("arial", 12, "bold"), padx=5, pady=5)
        self.report_results_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.report_treeview = ttk.Treeview(self.report_results_frame)
        self.report_treeview.pack(fill="both", expand=1)

        self.update_report_ui() # Initial UI update based on default selection

    def update_report_ui(self, event=None):
        selected_type = self.var_report_type.get()
        if selected_type == "Daily Revenue Report":
            self.lbl_report_date.grid(row=1, column=0, sticky=W, padx=5, pady=5)
            self.entry_report_date.grid(row=1, column=1, padx=5, pady=5)
        else:
            self.lbl_report_date.grid_forget()
            self.entry_report_date.grid_forget()

    def generate_selected_report(self):
        report_type = self.var_report_type.get()
        report_date_str = self.var_report_date.get()
        report_date_obj = None

        if report_type == "Daily Revenue Report":
            if not report_date_str:
                messagebox.showerror("Input Error", "Please provide a report date for Daily Revenue Report.", parent=self.report_window)
                return
            try:
                report_date_obj = datetime.strptime(report_date_str, "%d/%m/%Y").date()
            except ValueError:
                messagebox.showerror("Invalid Date", "Report Date must be in DD/MM/YYYY format.", parent=self.report_window)
                return
        else: # For Occupancy Report, report_date_obj is simply today's date
            report_date_obj = date.today()

        # Log the report generation (creates an "entity" entry)
        self.log_report_generation(report_type, report_date_obj, "Admin") # You can pass an actual user here

        # Clear previous treeview content
        for item in self.report_treeview.get_children():
            self.report_treeview.delete(item)

        if report_type == "Occupancy Report":
            self.generate_occupancy_report()
        elif report_type == "Daily Revenue Report":
            self.generate_daily_revenue_report(report_date_obj)


    def log_report_generation(self, report_type, report_date, generated_by):
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="11223344", database="hotel")
            my_cursor = conn.cursor()
            query = "INSERT INTO reports (report_type, report_date, generated_by) VALUES (%s, %s, %s)"
            values = (report_type, report_date, generated_by)
            my_cursor.execute(query, values)
            conn.commit()
            conn.close()
            # messagebox.showinfo("Log", "Report generation logged successfully.") # Optional: For debugging
        except Exception as e:
            messagebox.showerror("DB Log Error", f"Failed to log report generation: {str(e)}")

    def generate_occupancy_report(self):
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="11223344", database="hotel")
            my_cursor = conn.cursor()

            # 1. Total Rooms
            my_cursor.execute("SELECT COUNT(roomno) FROM details")
            total_rooms = my_cursor.fetchone()[0]

            # 2. Occupied Rooms (based on current date)
            today = date.today()
            # Select room_no from 'room' table where checkin <= today and checkout > today
            # Use DISTINCT because a room might appear multiple times if booked across multiple entries
            my_cursor.execute("""
                SELECT COUNT(DISTINCT roomavailable)
                FROM room
                WHERE STR_TO_DATE(checkin, '%d/%m/%Y') <= %s AND STR_TO_DATE(checkout, '%d/%m/%Y') > %s
            """, (today, today))
            occupied_rooms = my_cursor.fetchone()[0]

            available_rooms = total_rooms - occupied_rooms

            # Occupancy Rate
            occupancy_rate = (occupied_rooms / total_rooms * 100) if total_rooms > 0 else 0

            # 3. Occupancy by Room Type
            # Fetch all room types and their counts from 'details' table
            my_cursor.execute("SELECT roomtype, COUNT(roomno) FROM details GROUP BY roomtype")
            all_room_types_data = my_cursor.fetchall()
            all_room_types_dict = {rt: count for rt, count in all_room_types_data}

            # Fetch currently occupied rooms with their types
            my_cursor.execute(f"""
                SELECT d.roomtype, COUNT(DISTINCT r.roomavailable)
                FROM room r
                JOIN details d ON r.roomavailable = d.roomno
                WHERE STR_TO_DATE(r.checkin, '%d/%m/%Y') <= %s AND STR_TO_DATE(r.checkout, '%d/%m/%Y') > %s
                GROUP BY d.roomtype
            """, (today, today))
            occupied_room_types_data = my_cursor.fetchall()
            occupied_room_types_dict = {rt: count for rt, count in occupied_room_types_data}

            # Prepare data for Treeview
            columns = ("Metric", "Value")
            self.report_treeview["columns"] = columns
            self.report_treeview.heading("Metric", text="Metric")
            self.report_treeview.heading("Value", text="Value")
            self.report_treeview["show"] = "headings"
            self.report_treeview.column("Metric", width=200, anchor="w")
            self.report_treeview.column("Value", width=150, anchor="w")

            self.report_treeview.insert("", END, values=("Total Rooms", total_rooms))
            self.report_treeview.insert("", END, values=("Occupied Rooms", occupied_rooms))
            self.report_treeview.insert("", END, values=("Available Rooms", available_rooms))
            self.report_treeview.insert("", END, values=("Occupancy Rate", f"{occupancy_rate:.2f}%"))
            self.report_treeview.insert("", END, values=("", "")) # Separator
            self.report_treeview.insert("", END, values=("--- By Room Type ---", ""))

            for room_type, total_count in all_room_types_dict.items():
                occupied_count = occupied_room_types_dict.get(room_type, 0)
                available_count = total_count - occupied_count
                self.report_treeview.insert("", END, values=(f"{room_type} (Occupied)", occupied_count))
                self.report_treeview.insert("", END, values=(f"{room_type} (Available)", available_count))

            conn.close()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error generating occupancy report: {err}", parent=self.report_window)
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}", parent=self.report_window)

    def generate_daily_revenue_report(self, report_date):
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="11223344", database="hotel")
            my_cursor = conn.cursor()

            # Get bookings that were active on the report_date
            # The query should fetch all necessary columns, including roomavailable
            my_cursor.execute("""
                SELECT roomtype, meal, noofdays, checkin, checkout, roomavailable, TotalAmount
                FROM room
            """)
            all_bookings = my_cursor.fetchall()

            total_room_revenue = 0
            total_meal_revenue = 0
            total_tax_collected = 0
            processed_rooms = set()  # To count distinct rooms active on this day

            room_prices = {"Single": 1000, "Double": 1500, "Luxury": 2500, "Duplex": 3500}
            meal_prices = {"Breakfast": 300, "Lunch": 500, "Dinner": 700, "": 0}

            for booking in all_bookings:
                room_type, meal, noofdays_str, checkin_str, checkout_str, room_no, total_booking_amount_str = booking

                try:
                    # Convert checkin and checkout strings to datetime.date objects
                    booking_checkin = datetime.strptime(checkin_str, "%d/%m/%Y").date()
                    booking_checkout = datetime.strptime(checkout_str, "%d/%m/%Y").date()
                except ValueError:
                    # Skip this booking if dates are malformed
                    print(f"Skipping booking due to invalid date format: {booking}")
                    continue

                try:
                    num_of_days = int(noofdays_str) if noofdays_str else 1  # Handle potential empty string for noofdays
                    if num_of_days == 0:
                        num_of_days = 1
                except ValueError:
                    num_of_days = 1  # Fallback if noofdays is not an integer

                # Determine if this booking is active on the report_date
                # A booking is active if:
                # 1. It starts on or before report_date AND ends after report_date (multi-day stay)
                # 2. It starts and ends on the report_date (same-day stay)
                is_active_on_report_date = False
                if booking_checkin <= report_date and booking_checkout > report_date:
                    is_active_on_report_date = True
                elif booking_checkin == report_date and booking_checkout == report_date:
                    is_active_on_report_date = True


                if is_active_on_report_date:
                    room_cost_per_day = room_prices.get(room_type, 0)
                    meal_cost_per_day = meal_prices.get(meal, 0)

                    # For daily revenue, we account for the daily rate if the room is active.
                    # If it's a same-day stay, the full cost applies to that day.
                    if booking_checkin == report_date and booking_checkout == report_date:
                        # For a single-day booking, the entire cost contributes to this day
                        # Calculate daily cost components from total booking amount if possible for accuracy
                        try:
                            total_booking_amount = float(total_booking_amount_str)
                            # Assuming 10% tax. If total = sub_total * 1.1, then sub_total = total / 1.1
                            sub_total_for_booking = total_booking_amount / 1.1
                            tax_for_booking = total_booking_amount - sub_total_for_booking

                            # Distribute sub_total between room and meal based on their proportions
                            # This is a simplification; a more complex system would store daily charges.
                            # For simplicity, we can just take the total_booking_amount and divide it by the number of days.
                            # OR, we can continue with the per-day logic and add tax separately for the day.
                            daily_sub_total = room_cost_per_day + meal_cost_per_day
                            daily_tax_contribution = daily_sub_total * 0.10 # 10% tax per day
                            daily_room_revenue_contribution = room_cost_per_day
                            daily_meal_revenue_contribution = meal_cost_per_day

                            total_room_revenue += daily_room_revenue_contribution
                            total_meal_revenue += daily_meal_revenue_contribution
                            total_tax_collected += daily_tax_contribution
                        except ValueError:
                            # Fallback if total_booking_amount_str is invalid
                            daily_room_revenue_contribution = room_cost_per_day
                            daily_meal_revenue_contribution = meal_cost_per_day
                            daily_total_contribution = daily_room_revenue_contribution + daily_meal_revenue_contribution
                            daily_tax_contribution = daily_total_contribution * 0.1  # 10% tax
                            total_room_revenue += daily_room_revenue_contribution
                            total_meal_revenue += daily_meal_revenue_contribution
                            total_tax_collected += daily_tax_contribution

                    else:  # Multi-day stay active on report_date
                        # Each day contributes its daily rate
                        daily_room_revenue_contribution = room_cost_per_day
                        daily_meal_revenue_contribution = meal_cost_per_day
                        daily_total_contribution = daily_room_revenue_contribution + daily_meal_revenue_contribution
                        daily_tax_contribution = daily_total_contribution * 0.1  # 10% tax

                        total_room_revenue += daily_room_revenue_contribution
                        total_meal_revenue += daily_meal_revenue_contribution
                        total_tax_collected += daily_tax_contribution

                    processed_rooms.add(room_no)  # Add room to set of active rooms

            gross_daily_revenue = total_room_revenue + total_meal_revenue + total_tax_collected
            num_rooms_booked_on_day = len(processed_rooms) # Number of unique rooms with active bookings

            # Prepare data for Treeview
            columns = ("Metric", "Value")
            self.report_treeview["columns"] = columns
            self.report_treeview.heading("Metric", text="Metric")
            self.report_treeview.heading("Value", text="Value")
            self.report_treeview["show"] = "headings"
            self.report_treeview.column("Metric", width=200, anchor="w")
            self.report_treeview.column("Value", width=150, anchor="w")

            self.report_treeview.insert("", END, values=("Report Date", report_date.strftime("%d/%m/%Y")))
            self.report_treeview.insert("", END, values=("Total Room Revenue", f"{total_room_revenue:.2f}"))
            self.report_treeview.insert("", END, values=("Total Meal Revenue", f"{total_meal_revenue:.2f}"))
            self.report_treeview.insert("", END, values=("Total Tax Collected", f"{total_tax_collected:.2f}"))
            self.report_treeview.insert("", END, values=("Gross Daily Revenue", f"{gross_daily_revenue:.2f}"))
            self.report_treeview.insert("", END, values=("Number of Rooms Booked", num_rooms_booked_on_day))

            conn.close()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error generating daily revenue report: {err}", parent=self.report_window)
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}", parent=self.report_window)


if __name__ == '__main__':
    root = Tk()
    obj = HotelManagementSystem(root)
    root.mainloop()