import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import os


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "bususer"),
    "password": os.getenv("DB_PASSWORD", "YOUR_PASSWORD"),
    "database": os.getenv("DB_NAME", "bus_tracker")
}


def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


# ============================================================
# APPLICATION
# ============================================================

class BusTrackerGUI:

    def __init__(self, root):

        self.root = root

        self.root.title("KIIT BUS TRACKER")
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)

        self.root.configure(bg="#111111")

        self.create_styles()
        self.create_interface()

        self.load_dashboard()

    # ========================================================
    # STYLES
    # ========================================================

    def create_styles(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Treeview",
            background="#1c1c1c",
            foreground="white",
            fieldbackground="#1c1c1c",
            rowheight=30,
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            background="#d4af37",
            foreground="black",
            font=("Arial", 10, "bold")
        )

        style.map(
            "Treeview",
            background=[
                ("selected", "#555555")
            ],
            foreground=[
                ("selected", "white")
            ]
        )

    # ========================================================
    # MAIN INTERFACE
    # ========================================================

    def create_interface(self):

        # Header
        header = tk.Frame(
            self.root,
            bg="#111111",
            height=80
        )

        header.pack(
            fill="x",
            padx=20,
            pady=(15, 5)
        )

        title = tk.Label(
            header,
            text="KIIT BUS TRACKER",
            bg="#111111",
            fg="#d4af37",
            font=("Arial", 24, "bold")
        )

        title.pack(anchor="w")

        subtitle = tk.Label(
            header,
            text="Bus tracking and database management",
            bg="#111111",
            fg="#aaaaaa",
            font=("Arial", 10)
        )

        subtitle.pack(anchor="w")

        # Button bar
        button_frame = tk.Frame(
            self.root,
            bg="#111111"
        )

        button_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        buttons = [
            ("Buses", self.view_buses),
            ("Routes", self.view_routes),
            ("Route Stops", self.view_route_stops),
            ("Schedule", self.view_schedule),
            ("Refresh", self.load_dashboard)
        ]

        for text, command in buttons:

            button = tk.Button(
                button_frame,
                text=text,
                command=command,
                bg="#222222",
                fg="#d4af37",
                activebackground="#333333",
                activeforeground="white",
                relief="flat",
                bd=0,
                padx=18,
                pady=9,
                font=("Arial", 10, "bold"),
                cursor="hand2"
            )

            button.pack(
                side="left",
                padx=(0, 8)
            )

        # Search area
        search_frame = tk.Frame(
            self.root,
            bg="#111111"
        )

        search_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 10)
        )

        tk.Label(
            search_frame,
            text="Route ID:",
            bg="#111111",
            fg="white",
            font=("Arial", 10)
        ).pack(side="left")

        self.route_entry = tk.Entry(
            search_frame,
            bg="#222222",
            fg="white",
            insertbackground="white",
            relief="flat",
            font=("Arial", 10),
            width=10
        )

        self.route_entry.pack(
            side="left",
            padx=8,
            ipady=5
        )

        tk.Button(
            search_frame,
            text="Search Route",
            command=self.route_lookup,
            bg="#d4af37",
            fg="black",
            activebackground="#e5c158",
            relief="flat",
            bd=0,
            padx=14,
            pady=7,
            font=("Arial", 10, "bold"),
            cursor="hand2"
        ).pack(side="left")

        # Main content
        content = tk.Frame(
            self.root,
            bg="#111111"
        )

        content.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        self.tree = ttk.Treeview(
            content,
            show="headings"
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = ttk.Scrollbar(
            content,
            orient="vertical",
            command=self.tree.yview
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        # Status bar
        self.status = tk.Label(
            self.root,
            text="Ready",
            bg="#181818",
            fg="#aaaaaa",
            anchor="w",
            padx=20,
            pady=7,
            font=("Arial", 9)
        )

        self.status.pack(
            fill="x",
            side="bottom"
        )

    # ========================================================
    # TREEVIEW HELPER
    # ========================================================

    def display_data(self, columns, rows):

        self.tree.delete(*self.tree.get_children())

        self.tree["columns"] = columns

        for column in columns:

            self.tree.heading(
                column,
                text=column
            )

            self.tree.column(
                column,
                width=150,
                anchor="center"
            )

        for row in rows:
            self.tree.insert(
                "",
                "end",
                values=row
            )

        self.status.config(
            text=f"{len(rows)} record(s)"
        )

    # ========================================================
    # LOAD DASHBOARD
    # ========================================================

    def load_dashboard(self):

        try:

            db = get_db_connection()
            cursor = db.cursor()

            cursor.execute("""
                SELECT
                    bus_id,
                    bus_number,
                    capacity,
                    current_lat,
                    current_lng,
                    last_updated
                FROM buses
                ORDER BY bus_id
            """)

            rows = cursor.fetchall()

            self.display_data(
                (
                    "Bus ID",
                    "Bus Number",
                    "Capacity",
                    "Latitude",
                    "Longitude",
                    "Last Updated"
                ),
                rows
            )

            cursor.close()
            db.close()

        except mysql.connector.Error as error:

            self.show_database_error(error)

    # ========================================================
    # VIEW BUSES
    # ========================================================

    def view_buses(self):

        try:

            db = get_db_connection()
            cursor = db.cursor()

            cursor.execute("""
                SELECT
                    bus_id,
                    bus_number,
                    capacity,
                    current_lat,
                    current_lng,
                    last_updated
                FROM buses
                ORDER BY bus_id
            """)

            rows = cursor.fetchall()

            self.display_data(
                (
                    "Bus ID",
                    "Bus Number",
                    "Capacity",
                    "Latitude",
                    "Longitude",
                    "Last Updated"
                ),
                rows
            )

            cursor.close()
            db.close()

        except mysql.connector.Error as error:

            self.show_database_error(error)

    # ========================================================
    # VIEW ROUTES
    # ========================================================

    def view_routes(self):

        try:

            db = get_db_connection()
            cursor = db.cursor()

            cursor.execute("""
                SELECT
                    route_id,
                    route_name,
                    start_stop,
                    end_stop
                FROM routes
                ORDER BY route_id
            """)

            rows = cursor.fetchall()

            self.display_data(
                (
                    "Route ID",
                    "Route Name",
                    "Start Stop",
                    "End Stop"
                ),
                rows
            )

            cursor.close()
            db.close()

        except mysql.connector.Error as error:

            self.show_database_error(error)

    # ========================================================
    # VIEW ROUTE STOPS
    # ========================================================

    def view_route_stops(self):

        try:

            db = get_db_connection()
            cursor = db.cursor()

            cursor.execute("""
                SELECT
                    rs.route_id,
                    r.route_name,
                    rs.stop_order,
                    s.stop_name,
                    s.lat,
                    s.lng
                FROM route_stops rs
                JOIN routes r
                    ON rs.route_id = r.route_id
                JOIN stops s
                    ON rs.stop_id = s.stop_id
                ORDER BY
                    rs.route_id,
                    rs.stop_order
            """)

            rows = cursor.fetchall()

            self.display_data(
                (
                    "Route ID",
                    "Route Name",
                    "Stop Order",
                    "Stop Name",
                    "Latitude",
                    "Longitude"
                ),
                rows
            )

            cursor.close()
            db.close()

        except mysql.connector.Error as error:

            self.show_database_error(error)

    # ========================================================
    # VIEW SCHEDULE
    # ========================================================

    def view_schedule(self):

        try:

            db = get_db_connection()
            cursor = db.cursor()

            cursor.execute("""
                SELECT
                    s.schedule_id,
                    b.bus_number,
                    d.driver_name,
                    r.route_name,
                    s.departure_time
                FROM schedules s
                LEFT JOIN buses b
                    ON s.bus_id = b.bus_id
                LEFT JOIN drivers d
                    ON s.driver_id = d.driver_id
                JOIN routes r
                    ON s.route_id = r.route_id
                ORDER BY s.departure_time
            """)

            rows = cursor.fetchall()

            self.display_data(
                (
                    "Schedule ID",
                    "Bus",
                    "Driver",
                    "Route",
                    "Departure"
                ),
                rows
            )

            cursor.close()
            db.close()

        except mysql.connector.Error as error:

            self.show_database_error(error)

    # ========================================================
    # ROUTE LOOKUP
    # ========================================================

    def route_lookup(self):

        route_id = self.route_entry.get().strip()

        if not route_id:
            messagebox.showwarning(
                "Input Required",
                "Please enter a Route ID."
            )
            return

        try:
            route_id = int(route_id)

        except ValueError:

            messagebox.showerror(
                "Invalid Input",
                "Route ID must be a number."
            )

            return

        try:

            db = get_db_connection()
            cursor = db.cursor()

            cursor.execute("""
                SELECT
                    rs.route_id,
                    r.route_name,
                    rs.stop_order,
                    s.stop_name,
                    s.location,
                    s.lat,
                    s.lng
                FROM route_stops rs
                JOIN routes r
                    ON rs.route_id = r.route_id
                JOIN stops s
                    ON rs.stop_id = s.stop_id
                WHERE rs.route_id = %s
                ORDER BY rs.stop_order
            """, (route_id,))

            rows = cursor.fetchall()

            if not rows:

                messagebox.showinfo(
                    "No Results",
                    f"No stops found for Route {route_id}."
                )

                cursor.close()
                db.close()

                return

            self.display_data(
                (
                    "Route ID",
                    "Route Name",
                    "Stop Order",
                    "Stop Name",
                    "Location",
                    "Latitude",
                    "Longitude"
                ),
                rows
            )

            cursor.close()
            db.close()

        except mysql.connector.Error as error:

            self.show_database_error(error)

    # ========================================================
    # DATABASE ERROR
    # ========================================================

    def show_database_error(self, error):

        self.status.config(
            text="Database connection error"
        )

        messagebox.showerror(
            "Database Error",
            str(error)
        )


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

def main():

    root = tk.Tk()

    BusTrackerGUI(root)

    root.mainloop()


if __name__ == "__main__":
    main()
