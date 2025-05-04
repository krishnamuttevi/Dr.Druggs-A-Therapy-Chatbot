from flask import Flask, render_template_string

app = Flask(__name__)

# Dictionary for source locations
sources = {
    "Current Location": {"lat": 0, "lon": 0}  # Special option; coordinates determined via geolocation
}

# Dictionary for destination locations (with actual lat/lon values)
destinations = {

}

html_code = '''
<!DOCTYPE html>
<html>
<head>
  <title>Dynamic Route Selector</title>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  
  <style>
    /* Basic reset and font */
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }
    body {
      font-family: Arial, sans-serif;
      background-color: #FBF5E5;
      color: #212121;
    }
    
    /* Flex container for sidebar + map */
    .container {
      display: flex;
      min-height: 100vh;
    }
    
    /* Sidebar styles */
    .sidebar {
      width: 350px;
      padding: 20px;
      background-color: #FBF5E5;
      border-right: 2px solid #212121;
    }
    
    .sidebar h2 {
      color: #A35C7A;
      margin-bottom: 20px;
    }
    
    .controls {
      margin-bottom: 20px;
    }
    label {
      margin-right: 10px;
      font-weight: bold;
    }
    select {
      margin-right: 20px;
      padding: 5px;
      border: 1px solid #A35C7A;
      border-radius: 4px;
    }
    button {
      background-color: #C890A7;
      color: #FBF5E5;
      border: none;
      padding: 8px 16px;
      margin-right: 10px;
      border-radius: 4px;
      cursor: pointer;
      font-weight: bold;
    }
    button:hover {
      background-color: #A35C7A;
    }
    
    /* Styling for Dr.Druggs Box */
    .drdruggs-box {
      margin: 20px 0;
      padding: 15px;
      background: linear-gradient(135deg, #ffe0f0, #ffcce0);
      border: 2px dashed #A35C7A;
      border-radius: 8px;
      text-align: center;
      font-weight: bold;
      color: #A35C7A;
      cursor: pointer;
      transition: transform 0.2s;
    }
    .drdruggs-box:hover {
      transform: scale(1.05);
    }
    
    /* Table styling */
    table {
      border-collapse: collapse;
      width: 100%;
      margin-top: 10px;
    }
    th, td {
      border: 1px solid #212121;
      padding: 8px;
      text-align: left;
    }
    th {
      background-color: #C890A7;
      color: #FBF5E5;
    }
    tr:nth-child(even) {
      background-color: #F2E9E1;
    }
    tr:nth-child(odd) {
      background-color: #FFFFFF;
    }
    tr:hover {
      background-color: #C890A7;
      color: #FBF5E5;
      cursor: pointer;
    }
    
    /* Map container styles */
    .map-container {
      flex: 1; 
      position: relative;
    }
    #map {
      width: 100%;
      height: 100vh;
    }
  </style>
</head>

<body>
  <div class="container">
    <!-- Sidebar -->
    <div class="sidebar">
      <h2>Select Starting Location and Destination</h2>
      
      <div class="controls">
        <label for="sourceSelect">Source:</label>
        <select id="sourceSelect">
          {% for src, coords in sources.items() %}
            <option value="{{ src }}">{{ src }}</option>
          {% endfor %}
        </select>
        
        <br><br>
        
        <label for="destinationSelect">Destination:</label>
        <select id="destinationSelect">
          {% for dest, coords in destinations.items() %}
            <option value="{{ dest }}">{{ dest }}</option>
          {% endfor %}
        </select>
        
        <br><br>
        
        <button onclick="initMap()">Get Route</button>
        <button onclick="resetMap()">Reset Map</button>
      </div>
      
      <!-- Dr.Druggs creative box -->
      <div class="drdruggs-box" onclick="askDrDruggs()">
        Ask Dr.Druggs for a Surprise Destination!
      </div>

      <!-- Table of destinations: no lat/long columns -->
      <table>
        <thead>
          <tr>
            <th>Destination Name</th>
          </tr>
        </thead>
        <tbody>
          {% for dest, coords in destinations.items() %}
          <tr onclick="handleDestinationClick('{{ dest }}')">
            <td>{{ dest }}</td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
    </div>

    <!-- Map area -->
    <div class="map-container">
      <div id="map"></div>
    </div>
  </div>
  
  <!-- Leaflet JS -->
  <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
  <script>
    // Dictionaries passed from Flask (as JSON)
    const sourceDict = {{ sources | tojson | safe }};
    const destinationDict = {{ destinations | tojson | safe }};
    
    // Global variable for the map instance
    let map;

    // Remove any existing map instance and clear the container
    function resetMap() {
      if (map) {
        map.remove();
      }
      document.getElementById("map").innerHTML = "";
    }

    // Initialize the map and get the route based on user selections
    function initMap() {
      resetMap();  // Refresh the map each time
      
      // Get selected source and destination values
      const sourceSelect = document.getElementById("sourceSelect");
      const destinationSelect = document.getElementById("destinationSelect");
      const selectedSource = sourceSelect.value;
      const selectedDestination = destinationSelect.value;
      
      // Check if the source is "Current Location"
      if (selectedSource === "Current Location") {
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(position => {
            const startLat = position.coords.latitude;
            const startLon = position.coords.longitude;
            proceedWithRoute(startLat, startLon, selectedSource, selectedDestination);
          }, showError);
        } else {
          alert("Geolocation is not supported by your browser.");
        }
      } else {
        // Otherwise, use coordinates from the dictionary
        const startLat = sourceDict[selectedSource].lat;
        const startLon = sourceDict[selectedSource].lon;
        proceedWithRoute(startLat, startLon, selectedSource, selectedDestination);
      }
    }
    
    // Display error if geolocation fails
    function showError(error) {
      alert("Error retrieving location: " + error.message);
    }
    
    // Once source and destination coordinates are determined, display the route
    function proceedWithRoute(startLat, startLon, sourceName, destinationName) {
      const destLat = destinationDict[destinationName].lat;
      const destLon = destinationDict[destinationName].lon;
      
      // Initialize the map centered at the source
      map = L.map('map').setView([startLat, startLon], 7);
      
      // Add the OpenStreetMap tile layer
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
      }).addTo(map);
      
      // Place markers for the source and destination
      L.marker([startLat, startLon]).addTo(map)
        .bindPopup('Source: ' + sourceName).openPopup();
      L.marker([destLat, destLon]).addTo(map)
        .bindPopup('Destination: ' + destinationName);
      
      // Build the OSRM API URL (OSRM requires coordinates in order: longitude,latitude)
      const osrmUrl = 'https://router.project-osrm.org/route/v1/driving/'
                      + startLon + ',' + startLat + ';'
                      + destLon + ',' + destLat
                      + '?overview=full&geometries=geojson';
      
      // Fetch routing data from OSRM API
      fetch(osrmUrl)
        .then(response => response.json())
        .then(data => {
          if (data.routes && data.routes.length > 0) {
            const route = data.routes[0];
            // Convert OSRM GeoJSON coordinates ([lon, lat]) to Leaflet format ([lat, lon])
            const latLngs = route.geometry.coordinates.map(coord => [coord[1], coord[0]]);
            
            // Draw the route as a polyline
            const routeLine = L.polyline(latLngs, {color: 'blue'}).addTo(map);
            
            // Adjust the map view to fit the route
            map.fitBounds(routeLine.getBounds());
          } else {
            console.error('No route found');
          }
        })
        .catch(error => console.error('Error fetching route:', error));
    }

    // Function to handle destination row clicks
    function handleDestinationClick(destName) {
      document.getElementById("destinationSelect").value = destName;
      initMap();
    }
    
    // Function for "Ask Dr.Druggs" box to select a random destination
    function askDrDruggs() {
      const destinationsKeys = Object.keys(destinationDict);
      const randomIndex = Math.floor(Math.random() * destinationsKeys.length);
      const randomDestination = destinationsKeys[randomIndex];
      
      // Set the destination select to the random destination
      document.getElementById("destinationSelect").value = randomDestination;
      
      // Optionally, alert the user about the selection
      alert("Dr.Druggs recommends: " + randomDestination);
      
      // Initialize the map with the new selection
      initMap();
    }
  </script>
</body>
</html>
'''

@app.route("/")
def index():
    return render_template_string(html_code, sources=sources, destinations=destinations)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5001, debug=True)
