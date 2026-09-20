from flask import Flask, render_template, jsonify, request
import mysql.connector
import os

app = Flask(__name__)


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
    """
    Create and return a new MySQL database connection.
    """
    return mysql.connector.connect(**DB_CONFIG)


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def index():
    return render_template("index.html")


# ============================================================
# GPS SENDER PAGE
# ============================================================

@app.route("/sender")
def sender():
    return render_template("sender.html")


# ============================================================
# UPDATE BUS GPS LOCATION
# ============================================================

@app.route("/update_location", methods=["POST"])
def update_location():
    """
    Receive the latest GPS coordinates from a bus.

    Expected JSON:
    {
        "bus_id": 1,
        "latitude": 20.3555,
        "longitude": 85.8172
    }
    """

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "No JSON data received"
            }), 400

        # ----------------------------------------------------
        # Validate required fields
        # ----------------------------------------------------

        if "bus_id" not in data:
            return jsonify({
                "success": False,
                "error": "bus_id is required"
            }), 400

        if "latitude" not in data:
            return jsonify({
                "success": False,
                "error": "latitude is required"
            }), 400

        if "longitude" not in data:
            return jsonify({
                "success": False,
                "error": "longitude is required"
            }), 400

        # ----------------------------------------------------
        # Convert values
        # ----------------------------------------------------

        try:
            bus_id = int(data["bus_id"])
            latitude = float(data["latitude"])
            longitude = float(data["longitude"])
        except (ValueError, TypeError):
            return jsonify({
                "success": False,
                "error": "Invalid bus_id, latitude or longitude"
            }), 400

        # ----------------------------------------------------
        # Validate GPS coordinate ranges
        # ----------------------------------------------------

        if not -90 <= latitude <= 90:
            return jsonify({
                "success": False,
                "error": "Invalid latitude"
            }), 400

        if not -180 <= longitude <= 180:
            return jsonify({
                "success": False,
                "error": "Invalid longitude"
            }), 400

        # ----------------------------------------------------
        # Connect to database
        # ----------------------------------------------------

        db = get_db_connection()
        cursor = db.cursor()

        # ----------------------------------------------------
        # Check whether bus exists
        # ----------------------------------------------------

        cursor.execute(
            "SELECT bus_id FROM buses WHERE bus_id = %s",
            (bus_id,)
        )

        bus = cursor.fetchone()

        if bus is None:
            cursor.close()
            db.close()

            return jsonify({
                "success": False,
                "error": f"Bus ID {bus_id} does not exist"
            }), 404

        # ----------------------------------------------------
        # Update GPS location
        # ----------------------------------------------------

        cursor.execute(
            """
            UPDATE buses
            SET
                current_lat = %s,
                current_lng = %s,
                last_updated = CURRENT_TIMESTAMP
            WHERE bus_id = %s
            """,
            (latitude, longitude, bus_id)
        )

        db.commit()

        cursor.close()
        db.close()

        return jsonify({
            "success": True,
            "message": "Bus location updated successfully",
            "bus_id": bus_id,
            "latitude": latitude,
            "longitude": longitude
        })

    except mysql.connector.Error as error:
        return jsonify({
            "success": False,
            "error": f"Database error: {error}"
        }), 500

    except Exception as error:
        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


# ============================================================
# GET CURRENT BUS LOCATION
# ============================================================

@app.route("/get_location", methods=["GET"])
def get_location():
    """
    Return the current location of every bus.

    Priority:
        1. Real GPS location
        2. Simulated route movement

    The response includes:
        source = "gps"
        or
        source = "simulation"
    """

    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        # ----------------------------------------------------
        # Get all buses
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT
                bus_id,
                bus_number,
                current_index,
                current_lat,
                current_lng,
                last_updated
            FROM buses
            ORDER BY bus_id
            """
        )

        buses = cursor.fetchall()

        result = []

        # ----------------------------------------------------
        # Process every bus
        # ----------------------------------------------------

        for bus in buses:

            # =================================================
            # REAL GPS LOCATION
            # =================================================

            if (
                bus["current_lat"] is not None
                and bus["current_lng"] is not None
            ):

                result.append({
                    "bus_id": bus["bus_id"],
                    "bus_number": bus["bus_number"],
                    "lat": float(bus["current_lat"]),
                    "lng": float(bus["current_lng"]),
                    "current_index": bus["current_index"],
                    "source": "gps",
                    "last_updated": (
                        bus["last_updated"].isoformat()
                        if bus["last_updated"]
                        else None
                    )
                })

                continue

            # =================================================
            # SIMULATION FALLBACK
            # =================================================

            cursor.execute(
                """
                SELECT route_id
                FROM schedules
                WHERE bus_id = %s
                LIMIT 1
                """,
                (bus["bus_id"],)
            )

            schedule = cursor.fetchone()

            if not schedule:
                continue

            route_id = schedule["route_id"]

            # ------------------------------------------------
            # Get route stops
            # ------------------------------------------------

            cursor.execute(
                """
                SELECT
                    s.stop_id,
                    s.stop_name,
                    s.lat,
                    s.lng,
                    rs.stop_order
                FROM route_stops rs
                JOIN stops s
                    ON rs.stop_id = s.stop_id
                WHERE rs.route_id = %s
                ORDER BY rs.stop_order
                """,
                (route_id,)
            )

            route_stops = cursor.fetchall()

            if not route_stops:
                continue

            # ------------------------------------------------
            # Find current simulated stop
            # ------------------------------------------------

            current_index = bus["current_index"] or 0

            stop = route_stops[
                current_index % len(route_stops)
            ]

            # ------------------------------------------------
            # Advance simulated position
            # ------------------------------------------------

            new_index = (
                current_index + 1
            ) % len(route_stops)

            cursor.execute(
                """
                UPDATE buses
                SET current_index = %s
                WHERE bus_id = %s
                """,
                (new_index, bus["bus_id"])
            )

            # ------------------------------------------------
            # Only use simulation if coordinates exist
            # ------------------------------------------------

            if (
                stop["lat"] is not None
                and stop["lng"] is not None
            ):

                result.append({
                    "bus_id": bus["bus_id"],
                    "bus_number": bus["bus_number"],
                    "lat": float(stop["lat"]),
                    "lng": float(stop["lng"]),
                    "current_index": current_index,
                    "source": "simulation",
                    "last_updated": None
                })

        db.commit()

        cursor.close()
        db.close()

        return jsonify(result)

    except mysql.connector.Error as error:
        return jsonify({
            "error": f"Database error: {error}"
        }), 500

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500


# ============================================================
# GET ROUTES AND STOPS
# ============================================================

@app.route("/get_routes", methods=["GET"])
def get_routes():

    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                rs.route_id,
                rs.stop_order,
                s.stop_id,
                s.stop_name,
                s.location,
                s.lat,
                s.lng
            FROM route_stops rs
            JOIN stops s
                ON rs.stop_id = s.stop_id
            ORDER BY
                rs.route_id,
                rs.stop_order
            """
        )

        rows = cursor.fetchall()

        cursor.close()
        db.close()

        routes = {}

        # ----------------------------------------------------
        # Organize stops by route
        # ----------------------------------------------------

        for row in rows:

            route_id = row["route_id"]

            if route_id not in routes:
                routes[route_id] = []

            routes[route_id].append({
                "stop_id": row["stop_id"],
                "stop_name": row["stop_name"],
                "location": row["location"],
                "lat": (
                    float(row["lat"])
                    if row["lat"] is not None
                    else None
                ),
                "lng": (
                    float(row["lng"])
                    if row["lng"] is not None
                    else None
                ),
                "stop_order": row["stop_order"]
            })

        return jsonify(routes)

    except mysql.connector.Error as error:
        return jsonify({
            "error": f"Database error: {error}"
        }), 500

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/health", methods=["GET"])
def health():

    try:
        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute("SELECT 1")
        cursor.fetchone()

        cursor.close()
        db.close()

        return jsonify({
            "status": "ok",
            "database": "connected"
        })

    except mysql.connector.Error as error:
        return jsonify({
            "status": "error",
            "database": "disconnected",
            "error": str(error)
        }), 500


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
