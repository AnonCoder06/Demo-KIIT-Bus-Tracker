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
# DISPLAY BUSES
# ============================================================

def view_buses():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

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

    buses = cursor.fetchall()

    print("\n========== BUSES ==========")

    if not buses:
        print("No buses found.")
    else:
        for bus in buses:
            print(f"\nBus ID      : {bus['bus_id']}")
            print(f"Bus Number  : {bus['bus_number']}")
            print(f"Capacity    : {bus['capacity']}")

            if bus["current_lat"] is not None:
                print(
                    f"Location    : "
                    f"{bus['current_lat']}, {bus['current_lng']}"
                )
            else:
                print("Location    : Not available")

            print(f"Last Updated: {bus['last_updated']}")

    cursor.close()
    db.close()


# ============================================================
# DISPLAY ROUTES
# ============================================================

def view_routes():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            route_id,
            route_name,
            start_stop,
            end_stop
        FROM routes
        ORDER BY route_id
    """)

    routes = cursor.fetchall()

    print("\n========== ROUTES ==========")

    if not routes:
        print("No routes found.")
    else:
        for route in routes:
            print(f"\nRoute ID   : {route['route_id']}")
            print(f"Route Name : {route['route_name']}")
            print(f"Start      : {route['start_stop']}")
            print(f"End        : {route['end_stop']}")

    cursor.close()
    db.close()


# ============================================================
# DISPLAY ROUTE STOPS
# ============================================================

def view_route_stops():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            rs.route_id,
            r.route_name,
            rs.stop_order,
            s.stop_id,
            s.stop_name,
            s.location,
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

    print("\n========== ROUTE STOPS ==========")

    if not rows:
        print("No route stops found.")
    else:
        current_route = None

        for row in rows:

            if row["route_id"] != current_route:
                current_route = row["route_id"]

                print(
                    f"\nRoute {row['route_id']}: "
                    f"{row['route_name']}"
                )

            print(
                f"  {row['stop_order']}. "
                f"{row['stop_name']}"
            )

            print(
                f"     Location: {row['location']}"
            )

            if row["lat"] is not None and row["lng"] is not None:
                print(
                    f"     Coordinates: "
                    f"{row['lat']}, {row['lng']}"
                )

    cursor.close()
    db.close()


# ============================================================
# DISPLAY SCHEDULE
# ============================================================

def view_schedule():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

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

    schedules = cursor.fetchall()

    print("\n========== SCHEDULE ==========")

    if not schedules:
        print("No schedules found.")
    else:
        for schedule in schedules:
            print(f"\nSchedule ID : {schedule['schedule_id']}")
            print(
                f"Bus         : "
                f"{schedule['bus_number'] or 'Not assigned'}"
            )
            print(
                f"Driver      : "
                f"{schedule['driver_name'] or 'Not assigned'}"
            )
            print(f"Route       : {schedule['route_name']}")
            print(f"Departure   : {schedule['departure_time']}")

    cursor.close()
    db.close()


# ============================================================
# ROUTE LOOKUP
# ============================================================

def route_lookup():
    route_id = input("\nEnter Route ID: ").strip()

    try:
        route_id = int(route_id)
    except ValueError:
        print("Invalid Route ID.")
        return

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            r.route_id,
            r.route_name,
            r.start_stop,
            r.end_stop
        FROM routes r
        WHERE r.route_id = %s
    """, (route_id,))

    route = cursor.fetchone()

    if not route:
        print("Route not found.")
        cursor.close()
        db.close()
        return

    print("\n========== ROUTE ==========")
    print(f"Route ID   : {route['route_id']}")
    print(f"Route Name : {route['route_name']}")
    print(f"Start      : {route['start_stop']}")
    print(f"End        : {route['end_stop']}")

    cursor.execute("""
        SELECT
            s.stop_name,
            s.location,
            s.lat,
            s.lng,
            rs.stop_order
        FROM route_stops rs
        JOIN stops s
            ON rs.stop_id = s.stop_id
        WHERE rs.route_id = %s
        ORDER BY rs.stop_order
    """, (route_id,))

    stops = cursor.fetchall()

    print("\nStops:")

    for stop in stops:
        print(
            f"{stop['stop_order']}. "
            f"{stop['stop_name']}"
        )

        if stop["lat"] is not None and stop["lng"] is not None:
            print(
                f"   Coordinates: "
                f"{stop['lat']}, {stop['lng']}"
            )

    cursor.close()
    db.close()


# ============================================================
# MAIN MENU
# ============================================================

def main():
    while True:

        print("\n")
        print("========================================")
        print("          KIIT BUS TRACKER")
        print("========================================")
        print("1. View Buses")
        print("2. View Routes")
        print("3. View Route Stops")
        print("4. View Schedule")
        print("5. Route Lookup")
        print("6. Exit")
        print("========================================")

        choice = input("Enter your choice: ").strip()

        try:

            if choice == "1":
                view_buses()

            elif choice == "2":
                view_routes()

            elif choice == "3":
                view_route_stops()

            elif choice == "4":
                view_schedule()

            elif choice == "5":
                route_lookup()

            elif choice == "6":
                print("\nExiting...")
                break

            else:
                print("\nInvalid choice.")

        except mysql.connector.Error as error:
            print(f"\nDatabase error: {error}")

        except Exception as error:
            print(f"\nError: {error}")


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
