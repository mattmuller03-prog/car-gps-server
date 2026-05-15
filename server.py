from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# store latest locations from all cars
locations = {}

# -----------------------------
# RECEIVE GPS UPDATES
# -----------------------------
@app.route("/update", methods=["POST"])
def update():
    data = request.json
    car_id = data.get("car_id")
    locations[car_id] = data
    return {"status": "ok"}

# -----------------------------
# PROVIDE ALL CAR LOCATIONS
# -----------------------------
@app.route("/locations")
def get_locations():
    return jsonify(locations)

# -----------------------------
# LIVE MAP PAGE
# -----------------------------
@app.route("/map")
def map_page():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Live GPS Map</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet"
              href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    </head>
    <body>
        <h2>Live GPS Map</h2>
        <div id="map" style="height: 90vh;"></div>

        <script>
        var greenIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png',
    shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

var redIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
    shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]

            var map = L.map('map').setView([40, -76], 12);

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 19
            }).addTo(map);

            var markers = {};

            function updateMarkers() {
    fetch('/locations')
        .then(r => r.json())
        .then(data => {
            const now = Date.now();

            for (const car in data) {
                const info = data[car];
                const lat = info.lat;
                const lon = info.lon;

                // Convert timestamp to milliseconds
                const lastUpdate = new Date(info.timestamp).getTime();
                const ageSeconds = (now - lastUpdate) / 1000;

                // Choose marker color
                const icon = ageSeconds > 120 ? redIcon : greenIcon;

                if (!markers[car]) {
                    markers[car] = L.marker([lat, lon], { icon: icon }).addTo(map);
                } else {
                    markers[car].setLatLng([lat, lon]);
                    markers[car].setIcon(icon);
                }

                markers[car].bindPopup(
                    car + "<br>" +
                    "Last update: " + Math.round(ageSeconds) + " sec ago<br>" +
                    "Speed: " + info.speed + "<br>" +
                    "Alt: " + info.alt
                );
            }
        });
}


            setInterval(updateMarkers, 1000);
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

app.run(host="0.0.0.0", port=5000)
