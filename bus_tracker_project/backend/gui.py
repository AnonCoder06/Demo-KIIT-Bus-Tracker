import tkinter as tk
from tkinter import ttk
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="bususer",
    password="BusUser@1234",
    database="bus_tracker"
)
cursor = conn.cursor()

BG="#0a0a0a"
PANEL="#111111"
ACCENT="#FFD700"
ACCENT_DIM="#998100"
FG="#FFFFFF"
FG_DIM="#888888"
BORDER="#2a2a2a"
ROW_ODD="#141414"
ROW_EVEN="#0f0f0f"
SEL_BG="#2a2200"
SEL_FG="#FFD700"

FONT_TITLE=("Courier New",17,"bold")
FONT_BTN=("Courier New",10,"bold")
FONT_TABLE=("Courier New",10)
FONT_HEADER=("Courier New",10,"bold")

root=tk.Tk()
root.title("KIIT BUS TRACKER")
root.geometry("820x520")
root.configure(bg=BG)
root.resizable(False,False)

scan_canvas=tk.Canvas(root,width=820,height=520,bg=BG,highlightthickness=0)
scan_canvas.place(x=0,y=0)

for y in range(0,520,4):
    scan_canvas.create_line(0,y,820,y,fill="#ffffff",stipple="gray12")

header=tk.Frame(root,bg=BG,height=64)
header.place(x=0,y=0,width=820)

tk.Frame(header,bg=ACCENT,width=4,height=64).place(x=0,y=0)

tk.Label(header,
text="◈  BHUBANESWAR BUS TRACKER",
font=FONT_TITLE,
bg=BG,
fg=ACCENT,
padx=16).place(x=10,y=14)

tk.Label(header,
text="REAL-TIME TRANSIT MANAGEMENT SYSTEM  //  v2.5",
font=("Courier New",8),
bg=BG,
fg=ACCENT_DIM).place(x=26,y=42)

tk.Label(header,
text="[ SYS:ONLINE ]",
font=("Courier New",8,"bold"),
bg=BG,
fg=ACCENT).place(x=680,y=24)

tk.Frame(root,bg=ACCENT,height=2).place(x=0,y=64,width=820)

btn_frame=tk.Frame(root,bg=PANEL,height=52)
btn_frame.place(x=0,y=66,width=820)

BUTTONS=[
("▸  VIEW BUSES","show_buses"),
("▸  VIEW ROUTES","show_routes"),
("▸  VIEW SCHEDULE","show_schedule"),
("▸  VIEW ROUTE STOPS","show_route_stops"),
]

def dispatch(name):
    {
    "show_buses":show_buses,
    "show_routes":show_routes,
    "show_schedule":show_schedule,
    "show_route_stops":show_route_stops
    }[name]()

def make_btn(parent,text,cmd_name,col):
    f=tk.Frame(parent,bg=ACCENT,padx=1,pady=1)
    f.grid(row=0,column=col,padx=(14 if col==0 else 8,0),pady=10)

    b=tk.Button(
    f,
    text=text,
    font=FONT_BTN,
    bg=PANEL,
    fg=ACCENT,
    activebackground=ACCENT,
    activeforeground=BG,
    relief="flat",
    cursor="hand2",
    width=18,
    pady=5,
    command=lambda n=cmd_name:dispatch(n)
    )
    b.pack()

    def on_enter(e):
        b.configure(bg=ACCENT,fg=BG)

    def on_leave(e):
        b.configure(bg=PANEL,fg=ACCENT)

    b.bind("<Enter>",on_enter)
    b.bind("<Leave>",on_leave)

for i,(txt,cmd) in enumerate(BUTTONS):
    make_btn(btn_frame,txt,cmd,i)

tk.Frame(root,bg=BORDER,height=1).place(x=0,y=118,width=820)

status_var=tk.StringVar(value="SELECT A VIEW  //  AWAITING INPUT")

tk.Label(root,
textvariable=status_var,
font=("Courier New",8),
bg=BG,
fg=ACCENT_DIM,
anchor="w",
padx=16).place(x=0,y=120,width=700,height=22)

row_count_var=tk.StringVar(value="ROWS: 0")

tk.Label(root,
textvariable=row_count_var,
font=("Courier New",8),
bg=BG,
fg=ACCENT_DIM,
anchor="e",
padx=16).place(x=700,y=120,width=120,height=22)

style=ttk.Style()
style.theme_use("clam")

style.configure("Futuristic.Treeview",
background=ROW_ODD,
fieldbackground=ROW_ODD,
foreground=FG,
rowheight=28,
font=FONT_TABLE,
borderwidth=0,
relief="flat")

style.configure("Futuristic.Treeview.Heading",
background=PANEL,
foreground=ACCENT,
font=FONT_HEADER,
relief="flat",
borderwidth=0,
padding=(8,6))

style.map("Futuristic.Treeview",
background=[("selected",SEL_BG)],
foreground=[("selected",SEL_FG)])

tree_frame=tk.Frame(root,bg=BORDER,padx=1,pady=1)
tree_frame.place(x=14,y=146,width=792,height=310)

inner=tk.Frame(tree_frame,bg=BG)
inner.pack(fill="both",expand=True)

tree=ttk.Treeview(inner,style="Futuristic.Treeview",show="headings")
tree.pack(side="left",fill="both",expand=True)

scrollbar=ttk.Scrollbar(inner,orient="vertical",command=tree.yview)
scrollbar.pack(side="right",fill="y")
tree.configure(yscrollcommand=scrollbar.set)

tree.tag_configure("odd",background=ROW_ODD)
tree.tag_configure("even",background=ROW_EVEN)

tk.Frame(root,bg=ACCENT,height=2).place(x=0,y=460,width=820)

tk.Label(root,
text="DB: bus_tracker@localhost   //   USER: bususer   //   SYSTEM READY",
font=("Courier New",7),
bg=BG,
fg=FG_DIM).place(x=14,y=464)

search_frame=tk.Frame(root,bg=BG)
search_frame.place(x=14,y=430)

tk.Label(search_frame,
text="SEARCH STOP:",
font=("Courier New",9,"bold"),
bg=BG,
fg=ACCENT).pack(side="left",padx=(0,10))

stop_entry=tk.Entry(search_frame,
font=("Courier New",10),
bg="#111111",
fg=FG,
insertbackground=ACCENT,
width=25,
relief="flat")
stop_entry.pack(side="left")

tk.Button(
search_frame,
text="FIND ROUTES",
font=("Courier New",9,"bold"),
bg=PANEL,
fg=ACCENT,
activebackground=ACCENT,
activeforeground=BG,
relief="flat",
padx=12,
command=lambda:search_stop()
).pack(side="left",padx=10)

def clear_table():
    for item in tree.get_children():
        tree.delete(item)

def populate(columns,rows,status_msg):
    clear_table()
    tree["columns"]=columns

    for col in columns:
        tree.heading(col,text=col.upper(),anchor="center")
        tree.column(col,anchor="center",
        width=max(120,780//len(columns)),
        stretch=True)

    for i,r in enumerate(rows):
        tag="even" if i%2==0 else "odd"
        tree.insert("", "end", values=r, tags=(tag,))

    status_var.set(status_msg)
    row_count_var.set(f"ROWS: {len(rows)}")

def show_buses():
    cursor.execute("SELECT * FROM buses")
    rows=cursor.fetchall()
    populate(("ID","Number","Capacity"),rows,
    "MODULE: BUSES  //  ALL REGISTERED VEHICLES")

def show_routes():
    cursor.execute("SELECT * FROM routes")
    rows=cursor.fetchall()
    populate(("ID","Route","Start","End"),rows,
    "MODULE: ROUTES  //  ACTIVE ROUTE REGISTRY")

def show_schedule():
    q="""
    SELECT buses.bus_number, drivers.driver_name,
    routes.route_name, schedules.departure_time
    FROM schedules
    JOIN buses ON schedules.bus_id=buses.bus_id
    JOIN drivers ON schedules.driver_id=drivers.driver_id
    JOIN routes ON schedules.route_id=routes.route_id
    """
    cursor.execute(q)
    rows=cursor.fetchall()
    populate(("Bus","Driver","Route","Time"),rows,
    "MODULE: SCHEDULE  //  LIVE DEPARTURE BOARD")

def show_route_stops():
    q="""
    SELECT routes.route_name,
    stops.stop_name,
    route_stops.stop_order
    FROM route_stops
    JOIN routes ON route_stops.route_id=routes.route_id
    JOIN stops ON route_stops.stop_id=stops.stop_id
    ORDER BY routes.route_id,route_stops.stop_order
    """
    cursor.execute(q)
    rows=cursor.fetchall()
    populate(("Route","Stop","Order"),rows,
    "MODULE: ROUTE STOPS  //  STOP SEQUENCE PER ROUTE")

def search_stop():
    stop=stop_entry.get()

    q="""
    SELECT stops.stop_name,routes.route_name
    FROM route_stops
    JOIN stops ON route_stops.stop_id=stops.stop_id
    JOIN routes ON route_stops.route_id=routes.route_id
    WHERE stops.stop_name LIKE %s
    ORDER BY routes.route_name
    """

    cursor.execute(q,("%"+stop+"%",))
    rows=cursor.fetchall()

    populate(("Stop","Route"),rows,
    "MODULE: STOP SEARCH  //  ROUTES SERVING STOP")

root.mainloop()
