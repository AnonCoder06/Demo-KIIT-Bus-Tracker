// ================== MAP INIT ==================
const map = L.map('map').setView([20.3174, 85.8190], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// ================== GLOBALS ==================
const busMarkers = {};
let routePath = [];


// ================== LOAD REAL ROAD ==================
function loadRoutes(){

    const url = "https://router.project-osrm.org/route/v1/driving/" +
        "85.8245,20.2961;" +
        "85.8190,20.3174;" +
        "85.8172,20.3555;" +
        "85.8162,20.3535;" +
        "85.8200,20.3605" +
        "?overview=full&geometries=geojson";

    fetch(url)
    .then(res => res.json())
    .then(data => {

        const coords = data.routes[0].geometry.coordinates;

        routePath = coords.map(c => [c[1], c[0]]);

        L.polyline(routePath, {
            color: 'blue',
            weight: 5,
            opacity: 0.8
        }).addTo(map);

    });
}


// ================== SHOW STOPS ==================
function loadStops(){
    fetch("/get_routes")
    .then(res => res.json())
    .then(data => {

        data.forEach(route => {

            route.stops.forEach(stop => {

                if(!stop.stop_name.startsWith("Mid_")){
                    L.circleMarker([stop.lat, stop.lng], {
                        radius: 6,
                        color: 'red'
                    })
                    .addTo(map)
                    .bindPopup("📍 " + stop.stop_name);
                }

            });

        });

    });
}


// ================== SMOOTH MOVEMENT ==================
function smoothMove(marker, start, end, steps = 25, delay = 20){

    if(!start){
        marker.setLatLng(end);
        return;
    }

    let i = 0;

    const latStep = (end[0] - start[0]) / steps;
    const lngStep = (end[1] - start[1]) / steps;

    const interval = setInterval(() => {

        if(i >= steps){
            clearInterval(interval);
            return;
        }

        const lat = start[0] + latStep * i;
        const lng = start[1] + lngStep * i;

        marker.setLatLng([lat, lng]);
        i++;

    }, delay);
}


// ================== BUS MOVEMENT ==================
function updateBusLocation(){

    if(routePath.length === 0) return;

    fetch("/get_location")
    .then(res => res.json())
    .then(data => {

        data.forEach(bus => {

            const id = bus.bus_id;

            const pathIndex = (bus.current_index * 10) % routePath.length;
            const newPos = routePath[pathIndex];

            if(!busMarkers[id]){

                const busIcon = L.icon({
                    iconUrl: "https://cdn-icons-png.flaticon.com/512/3448/3448339.png",
                    iconSize: [30, 30],
                    iconAnchor: [15, 15]
                });

                busMarkers[id] = L.marker(newPos, { icon: busIcon }).addTo(map);

                busMarkers[id].bindPopup(`
                    <b>Bus:</b> ${id}<br>
                    <b>Status:</b> Running
                `);

                busMarkers[id]._lastPos = newPos;

            } else {

                const oldPos = busMarkers[id]._lastPos;

                smoothMove(busMarkers[id], oldPos, newPos);

                busMarkers[id]._lastPos = newPos;
            }

        });

    });
}


// ================== RUN ==================
loadRoutes();
loadStops();
setInterval(updateBusLocation, 1000);