# KIIT Bus Tracker

A web-based bus tracking system designed for KIIT University to provide a centralized way to manage bus routes, stops, schedules, drivers, and bus locations.

The project combines a **JavaScript/Leaflet frontend**, **Flask backend**, and **MySQL database** to create the foundation for a campus transportation tracking platform.

---

## Features

* Interactive map using **Leaflet.js**
* OpenStreetMap-based map rendering
* Visualization of bus routes and stops
* Bus location tracking through a Flask API
* Smooth movement of bus markers on the map
* MySQL-backed transportation data
* Route, bus, driver, stop, and schedule management
* API endpoints for retrieving and updating bus locations
* KIIT/Bhubaneswar-focused route data

---

## Tech Stack

| Layer              | Technology                 |
| ------------------ | -------------------------- |
| Frontend           | HTML, CSS, JavaScript      |
| Mapping            | Leaflet.js                 |
| Map Data           | OpenStreetMap              |
| Backend            | Python, Flask              |
| Database           | MySQL                      |
| Database Connector | MySQL Connector for Python |

---

## Architecture

```text
                  ┌─────────────────────┐
                  │       User          │
                  │      Browser        │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Frontend            │
                  │ HTML/CSS/JavaScript │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Leaflet.js Map      │
                  │ + OpenStreetMap      │
                  └──────────┬──────────┘
                             │
                       HTTP / API
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Flask Backend       │
                  │ Python              │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ MySQL Database      │
                  └─────────────────────┘
```

The frontend communicates with the Flask backend through HTTP endpoints. The backend handles the application logic and database interaction, while Leaflet is responsible for displaying routes, stops, and bus markers.

---

## Database Design

The project follows a relational database structure for transportation management.

### Core Tables

| Table           | Purpose                                               |
| --------------- | ----------------------------------------------------- |
| `routes`        | Stores available bus routes                           |
| `buses`         | Stores bus information                                |
| `drivers`       | Stores driver information                             |
| `stops`         | Stores individual bus stops                           |
| `route_stops`   | Associates stops with routes and preserves stop order |
| `schedules`     | Stores bus schedules and timings                      |
| `bus_locations` | Stores bus latitude/longitude information             |

This separation keeps transportation entities modular and makes the system easier to extend.

---

## API

The Flask backend provides endpoints used by the frontend for bus tracking.

### `GET /get_location`

Retrieves the current bus location information used by the frontend.

### `/sender`

Used as part of the location-sender workflow for transmitting bus-location data to the backend.

### `POST /update_location`

Updates the stored location of a bus.

> Request parameters and response formats should be treated according to the current Flask implementation in the repository.

---

## Bus Location Flow

The intended data flow is:

```text
GPS / Location Source
        │
        ▼
 /update_location
        │
        ▼
     Flask
        │
        ▼
      MySQL
        │
        ▼
   /get_location
        │
        ▼
    Leaflet Map
        │
        ▼
  Bus Marker Update
```

The frontend can interpolate between coordinates to make bus movement visually smoother instead of instantly jumping between GPS positions.

A movement function such as `smoothMove()` is used for this purpose.

---

## Map Visualization

The project uses **Leaflet.js** for interactive geospatial visualization.

OpenStreetMap provides the underlying map tiles, while Leaflet handles:

* Map rendering
* Bus markers
* Route lines
* Stop markers
* Marker movement
* User interaction

Example:

```javascript
const map = L.map('map').setView([20.35, 85.82], 13);

L.tileLayer(
    'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
).addTo(map);
```

---

## Getting Started

### Prerequisites

Make sure you have:

* Python 3
* MySQL Server
* Git
* A modern web browser

Install the required Python dependencies:

```bash
pip install flask mysql-connector-python
```

---

### Clone the Repository

```bash
git clone https://github.com/AnonCoder06/Demo-KIIT-Bus-Tracker.git
cd Demo-KIIT-Bus-Tracker
```

---

### Configure MySQL

Create the project database:

```sql
CREATE DATABASE bus_tracker;
```

Then create/import the required tables and configure the Flask application with your MySQL credentials.

Example configuration:

```python
db = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="bus_tracker"
)
```

**Do not commit database passwords or other secrets to GitHub.**

Use environment variables for production deployments.

---

### Run the Backend

Start the Flask application using the project's backend entry point:

```bash
python3 app.py
```

The development server will normally be available at:

```text
http://127.0.0.1:5000
```

---

### Run the Frontend

Open the frontend entry page through the project's intended setup.

For a simple static frontend, you can also use Python's built-in server:

```bash
python3 -m http.server 5500
```

Then open:

```text
http://127.0.0.1:5500
```

---

## Project Structure

The exact structure may evolve as the project develops. A typical organization is:

```text
Demo-KIIT-Bus-Tracker/
│
├── frontend/
│   ├── index.html
│   ├── css/
│   └── js/
│       └── map.js
│
├── backend/
│   ├── app.py
│   └── ...
│
├── database/
│   └── schema.sql
│
├── README.md
└── ...
```

Use the actual repository structure as the source of truth when adding or documenting new modules.

---

## Development Workflow

A typical tracking cycle is:

1. A location source obtains the bus coordinates.
2. The coordinates are sent to the Flask backend.
3. Flask processes the request.
4. The location is stored or updated in MySQL.
5. The frontend requests the latest location.
6. Leaflet updates the corresponding bus marker.
7. Marker interpolation provides smoother visual movement.

---

## Current Scope

This repository is primarily a **prototype/demo of a campus bus tracking platform**.

It establishes the core components required for a larger transportation management system:

* Frontend map visualization
* Backend APIs
* Relational database design
* Route and stop representation
* Bus location updates

The system can later be extended into a production-ready platform.

---

## Future Improvements

Potential improvements include:

* Real GPS hardware integration
* WebSocket-based real-time updates
* Authentication and role-based access control
* Driver dashboard
* Admin dashboard
* Route and schedule management UI
* ETA calculation
* Bus occupancy information
* Location history and trip playback
* Notifications for students
* Improved API validation
* Database indexing and optimization
* Docker-based deployment
* Cloud deployment
* Automated testing
* CI/CD pipeline

---

## Learning Outcomes

This project demonstrates practical implementation of:

* **REST API development**
* **Frontend/backend integration**
* **Relational database design**
* **MySQL database connectivity**
* **Geospatial visualization**
* **JavaScript map development**
* **Real-time location handling**
* **Python Flask development**

---

## Contributing

Contributions and improvements are welcome.

### 1. Fork the repository

### 2. Create a feature branch

```bash
git checkout -b feature/your-feature
```

### 3. Commit your changes

```bash
git add .
git commit -m "Add your feature"
```

### 4. Push the branch

```bash
git push origin feature/your-feature
```

### 5. Open a Pull Request

---

## License

No license is currently specified for this project.

If you intend to make the project open source, consider adding an appropriate license such as MIT.

---

## Author

**Lipsit Naik**

GitHub: [@AnonCoder06](https://github.com/AnonCoder06)

---

## Acknowledgements

* [Leaflet.js](https://leafletjs.com/)
* [OpenStreetMap](https://www.openstreetmap.org/)
* [Flask](https://flask.palletsprojects.com/)
* [MySQL](https://www.mysql.com/)

---

**KIIT Bus Tracker — a foundation for smarter campus transportation.**
