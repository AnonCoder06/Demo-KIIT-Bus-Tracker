import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="bususer",
    password="BusPass123!",
    database="bus_tracker"
)

cursor = conn.cursor()

def view_buses():
    cursor.execute("SELECT * FROM buses")
    rows = cursor.fetchall()

    print("\nBus ID | Bus Number | Capacity")
    print("--------------------------------")

    for r in rows:
        print(f"{r[0]:6} | {r[1]:10} | {r[2]}")

def view_routes():
    cursor.execute("SELECT * FROM routes")
    rows = cursor.fetchall()

    print("\nRoute ID | Route Name | Start | End")
    print("--------------------------------------")

    for r in rows:
        print(f"{r[0]:8} | {r[1]:10} | {r[2]:12} | {r[3]}")

def view_route_stops():
    q = """
    SELECT routes.route_name, stops.stop_name, route_stops.stop_order
    FROM route_stops
    JOIN routes ON route_stops.route_id = routes.route_id
    JOIN stops ON route_stops.stop_id = stops.stop_id
    ORDER BY routes.route_id, route_stops.stop_order
    """
    cursor.execute(q)
    rows = cursor.fetchall()
    for r in rows:
        print(r)

def view_schedule():
    q = """
    SELECT buses.bus_number, drivers.driver_name, routes.route_name, schedules.departure_time
    FROM schedules
    JOIN buses ON schedules.bus_id = buses.bus_id
    JOIN drivers ON schedules.driver_id = drivers.driver_id
    JOIN routes ON schedules.route_id = routes.route_id
    """
    cursor.execute(q)
    rows = cursor.fetchall()

    print("\nBus | Driver | Route | Departure")
    print("----------------------------------")

    for r in rows:
        print(f"{r[0]:8} | {r[1]:15} | {r[2]:8} | {r[3]}")

def route_lookup():
    name = input("Route name: ")
    q = """
    SELECT stops.stop_name
    FROM route_stops
    JOIN routes ON route_stops.route_id = routes.route_id
    JOIN stops ON route_stops.stop_id = stops.stop_id
    WHERE routes.route_name = %s
    ORDER BY route_stops.stop_order
    """
    cursor.execute(q, (name,))
    rows = cursor.fetchall()
    for r in rows:
        print(r[0])

while True:
    print("\n==============================")
    print("   Bhubaneswar Bus Tracker")
    print("==============================")
    print("1. View Buses")
    print("2. View Routes")
    print("3. View Route Stops")
    print("4. View Schedule")
    print("5. Find Stops By Route")
    print("6. Exit")
    print("==============================")

    c = input("Choice: ")

    if c == "1":
        view_buses()
    elif c == "2":
        view_routes()
    elif c == "3":
        view_route_stops()
    elif c == "4":
        view_schedule()
    elif c == "5":
        route_lookup()
    elif c == "6":
        break