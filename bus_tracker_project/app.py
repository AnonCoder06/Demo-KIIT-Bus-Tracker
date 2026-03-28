from flask import Flask, jsonify, render_template
import mysql.connector

app = Flask(__name__)

# DB connection
db = mysql.connector.connect(
    host="localhost",
    user="bususer",
    password="BusUser@1234",
    database="bus_tracker"
)

cursor = db.cursor(dictionary=True, buffered=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sender")
def sender():
    return render_template("sender.html")


# ================== BUS MOVEMENT (DB) ==================
@app.route("/get_location")
def get_location():

    cursor.execute("SELECT bus_id, current_index FROM buses")
    buses = cursor.fetchall()

    for bus in buses:
        bus_id = bus["bus_id"]
        index = bus["current_index"]

        cursor.execute("SELECT route_id FROM schedules WHERE bus_id=%s", (bus_id,))
        route_data = cursor.fetchone()

        if not route_data:
            continue

        route_id = route_data["route_id"]

        cursor.execute("""
            SELECT s.lat, s.lng
            FROM route_stops rs
            JOIN stops s ON rs.stop_id = s.stop_id
            WHERE rs.route_id=%s
            ORDER BY rs.stop_order
        """, (route_id,))
        stops = cursor.fetchall()

        if not stops:
            continue

        index = (index + 1) % len(stops)

        cursor.execute("""
            UPDATE buses SET current_index=%s WHERE bus_id=%s
        """, (index, bus_id))

    db.commit()

    result = []

    cursor.execute("SELECT bus_id, current_index FROM buses")
    buses = cursor.fetchall()

    for bus in buses:
        bus_id = bus["bus_id"]
        index = bus["current_index"]

        cursor.execute("SELECT route_id FROM schedules WHERE bus_id=%s", (bus_id,))
        route_data = cursor.fetchone()

        if not route_data:
            continue

        route_id = route_data["route_id"]

        cursor.execute("""
            SELECT s.lat, s.lng
            FROM route_stops rs
            JOIN stops s ON rs.stop_id = s.stop_id
            WHERE rs.route_id=%s
            ORDER BY rs.stop_order
        """, (route_id,))
        stops = cursor.fetchall()

        if stops:
            result.append({
                "bus_id": bus_id,
                "lat": stops[index]["lat"],
                "lng": stops[index]["lng"],
                "current_index": index
            })

    return jsonify(result)


@app.route("/get_routes")
def get_routes():
    result = []

    cursor.execute("SELECT DISTINCT route_id FROM route_stops")
    routes = cursor.fetchall()

    for r in routes:
        route_id = r["route_id"]

        cursor.execute("""
            SELECT s.stop_name, s.lat, s.lng
            FROM route_stops rs
            JOIN stops s ON rs.stop_id = s.stop_id
            WHERE rs.route_id=%s
            ORDER BY rs.stop_order
        """, (route_id,))

        stops = cursor.fetchall()
        stops = [s for s in stops if s["lat"] and s["lng"]]

        result.append({
            "route_id": route_id,
            "stops": stops
        })

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
