// ============================================================
// KIIT BUS TRACKER - MAP
// ============================================================

// ------------------------------------------------------------
// CREATE MAP
// ------------------------------------------------------------

const map = L.map("map").setView(
    [20.3174, 85.8190],
    13
);


// ------------------------------------------------------------
// OPENSTREETMAP TILES
// ------------------------------------------------------------

L.tileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
        attribution:
            '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',

        maxZoom: 19
    }
).addTo(map);


// ============================================================
// GLOBAL VARIABLES
// ============================================================

let busMarkers = {};

let routeLayers = [];

let stopMarkers = [];


// ============================================================
// BUS ICON
// ============================================================

const busIcon = L.icon({

    iconUrl:
        "https://cdn-icons-png.flaticon.com/512/3448/3448339.png",

    iconSize: [40, 40],

    iconAnchor: [20, 20],

    popupAnchor: [0, -20]
});


// ============================================================
// LOAD ROUTES
// ============================================================

async function loadRoutes() {

    try {

        const response =
            await fetch("/get_routes");

        if (!response.ok) {

            throw new Error(
                `HTTP ${response.status}`
            );
        }

        const routes =
            await response.json();


        // ----------------------------------------------------
        // Remove previously drawn routes
        // ----------------------------------------------------

        routeLayers.forEach(
            layer => map.removeLayer(layer)
        );

        routeLayers = [];


        // ----------------------------------------------------
        // Draw every route
        // ----------------------------------------------------

        Object.entries(routes).forEach(
            ([routeId, stops]) => {

                const coordinates = [];

                stops.forEach(stop => {

                    if (
                        stop.lat !== null &&
                        stop.lng !== null
                    ) {

                        coordinates.push([
                            stop.lat,
                            stop.lng
                        ]);
                    }

                });


                if (coordinates.length < 2) {
                    return;
                }


                // ------------------------------------------------
                // Draw route using Leaflet straight segments
                // ------------------------------------------------

                const routeLine =
                    L.polyline(
                        coordinates,
                        {
                            weight: 5,
                            opacity: 0.75
                        }
                    ).addTo(map);


                routeLayers.push(routeLine);


                // ------------------------------------------------
                // Add route popup
                // ------------------------------------------------

                routeLine.bindPopup(
                    `<strong>Route ${routeId}</strong>`
                );
            }
        );

    }

    catch (error) {

        console.error(
            "Error loading routes:",
            error
        );
    }
}


// ============================================================
// LOAD BUS STOPS
// ============================================================

async function loadStops() {

    try {

        const response =
            await fetch("/get_routes");

        if (!response.ok) {

            throw new Error(
                `HTTP ${response.status}`
            );
        }

        const routes =
            await response.json();


        // ----------------------------------------------------
        // Remove existing stop markers
        // ----------------------------------------------------

        stopMarkers.forEach(
            marker => map.removeLayer(marker)
        );

        stopMarkers = [];


        // ----------------------------------------------------
        // Keep track of stops already displayed
        // ----------------------------------------------------

        const displayedStops =
            new Set();


        // ----------------------------------------------------
        // Add stops
        // ----------------------------------------------------

        Object.values(routes).forEach(
            stops => {

                stops.forEach(stop => {

                    if (
                        stop.lat === null ||
                        stop.lng === null
                    ) {
                        return;
                    }


                    // Avoid drawing duplicate stops
                    if (
                        displayedStops.has(
                            stop.stop_id
                        )
                    ) {
                        return;
                    }


                    displayedStops.add(
                        stop.stop_id
                    );


                    const marker =
                        L.circleMarker(
                            [
                                stop.lat,
                                stop.lng
                            ],
                            {
                                radius: 7,
                                weight: 2,
                                fillOpacity: 0.9
                            }
                        ).addTo(map);


                    marker.bindPopup(
                        `
                        <strong>${stop.stop_name}</strong>
                        <br>
                        ${stop.location || ""}
                        `
                    );


                    stopMarkers.push(marker);
                });
            }
        );

    }

    catch (error) {

        console.error(
            "Error loading stops:",
            error
        );
    }
}


// ============================================================
// SMOOTH BUS MOVEMENT
// ============================================================

function smoothMove(
    marker,
    start,
    end,
    steps = 20,
    delay = 50
) {

    if (!marker) {
        return;
    }


    const startLat =
        start[0];

    const startLng =
        start[1];

    const endLat =
        end[0];

    const endLng =
        end[1];


    let step = 0;


    function animate() {

        step++;


        const progress =
            step / steps;


        const lat =
            startLat +
            (endLat - startLat) *
            progress;


        const lng =
            startLng +
            (endLng - startLng) *
            progress;


        marker.setLatLng([
            lat,
            lng
        ]);


        if (step < steps) {

            setTimeout(
                animate,
                delay
            );
        }
    }


    animate();
}


// ============================================================
// UPDATE BUS LOCATIONS
// ============================================================

async function updateBusLocation() {

    try {

        const response =
            await fetch("/get_location");


        if (!response.ok) {

            throw new Error(
                `HTTP ${response.status}`
            );
        }


        const buses =
            await response.json();


        // ----------------------------------------------------
        // Process every bus
        // ----------------------------------------------------

        buses.forEach(bus => {

            // ------------------------------------------------
            // Validate coordinates
            // ------------------------------------------------

            if (
                bus.lat === null ||
                bus.lng === null ||
                bus.lat === undefined ||
                bus.lng === undefined
            ) {
                return;
            }


            const newPosition = [
                Number(bus.lat),
                Number(bus.lng)
            ];


            // ------------------------------------------------
            // Create marker if it doesn't exist
            // ------------------------------------------------

            if (!busMarkers[bus.bus_id]) {

                const marker =
                    L.marker(
                        newPosition,
                        {
                            icon: busIcon
                        }
                    ).addTo(map);


                busMarkers[
                    bus.bus_id
                ] = {
                    marker: marker,
                    position: newPosition
                };


                updateBusPopup(
                    busMarkers[bus.bus_id],
                    bus
                );


                return;
            }


            // ------------------------------------------------
            // Existing marker
            // ------------------------------------------------

            const busMarker =
                busMarkers[bus.bus_id];


            const oldPosition =
                busMarker.position;


            // ------------------------------------------------
            // Smoothly move marker
            // ------------------------------------------------

            smoothMove(
                busMarker.marker,
                oldPosition,
                newPosition,
                20,
                50
            );


            busMarker.position =
                newPosition;


            // ------------------------------------------------
            // Update popup
            // ------------------------------------------------

            updateBusPopup(
                busMarker,
                bus
            );
        });


    }

    catch (error) {

        console.error(
            "Error updating bus locations:",
            error
        );
    }
}


// ============================================================
// BUS POPUP
// ============================================================

function updateBusPopup(
    busMarker,
    bus
) {

    const source =
        bus.source === "gps"
            ? "Live GPS"
            : "Simulation";


    const sourceIcon =
        bus.source === "gps"
            ? "●"
            : "○";


    let lastUpdated =
        "Not available";


    if (bus.last_updated) {

        const date =
            new Date(
                bus.last_updated
            );


        lastUpdated =
            date.toLocaleString();
    }


    busMarker.marker.bindPopup(
        `
        <div style="min-width: 180px">

            <strong>
                Bus ${bus.bus_number}
            </strong>

            <hr>

            <b>Bus ID:</b>
            ${bus.bus_id}

            <br>

            <b>Source:</b>
            ${sourceIcon} ${source}

            <br>

            <b>Latitude:</b>
            ${Number(bus.lat).toFixed(6)}

            <br>

            <b>Longitude:</b>
            ${Number(bus.lng).toFixed(6)}

            <br>

            <b>Updated:</b>
            ${lastUpdated}

        </div>
        `
    );
}


// ============================================================
// INITIALIZE MAP
// ============================================================

async function initializeMap() {

    await loadRoutes();

    await loadStops();

    await updateBusLocation();

}


// ============================================================
// START
// ============================================================

initializeMap();


// ============================================================
// REFRESH BUS LOCATIONS
// ============================================================
//
// GPS positions are checked every 2 seconds.
//
// The frontend now uses the actual lat/lng returned by
// /get_location instead of calculating a fake position
// from the route path.
//

setInterval(
    updateBusLocation,
    2000
);
