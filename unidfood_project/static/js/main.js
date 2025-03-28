function loadGoogleMaps() {
    if (document.getElementById('googleMapsScript')) return; 

    const script = document.createElement('script');
    script.id = 'googleMapsScript';
    script.src = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyBbDMNNYSjosH4WOrB5YC_oG1IuzjB-eY8&libraries=places&callback=initMap';
    script.async = true;
    script.defer = true;
    document.body.appendChild(script);
}

function initMap() {
    const mapContainer = document.getElementById("map");
    if (!mapContainer) return;

    const map = new google.maps.Map(mapContainer, {
        center: { lat: 55.8784, lng: -4.2906 }, // Glasgow University Coordinates
        zoom: 14
    });
    
    fetchPlaces();
    const places_json = localStorage.getItem("placesData")
    const places = JSON.parse(places_json)

   
    document.querySelectorAll('.move-map-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const lat = parseFloat(this.getAttribute('data-lat'));
            const lng = parseFloat(this.getAttribute('data-lng'));
            map.setCenter({ lat: lat, lng: lng });
            map.setZoom(14);
        });
    });

    const input = document.getElementById("search-input");
    if (input) {
        const autocomplete = new google.maps.places.Autocomplete(input);
        autocomplete.addListener("place_changed", function () {
            const place = autocomplete.getPlace();
            if (!place.geometry || !place.geometry.location) return;

            map.setCenter(place.geometry.location);
            map.setZoom(15);

            new google.maps.Marker({
                position: place.geometry.location,
                map,
                title: place.name
            });
        });
    }
}

document.addEventListener("DOMContentLoaded", () => {
    if (document.getElementById("map")) {
        loadGoogleMaps();
    }

    const searchInput = document.getElementById("search");
    const resultsDiv = document.getElementById("results");

    if (searchInput && resultsDiv) {
        searchInput.addEventListener("keyup", function () {
            let query = searchInput.value.trim();
            if (query.length > 2) {
                fetch(`/search/?q=${query}`, {
                    method: "GET",
                    headers: { "X-Requested-With": "XMLHttpRequest" }
                })
                .then(response => response.json())
                .then(data => {
                    resultsDiv.innerHTML = "";
                    localStorage.setItem("searchResults", JSON.stringify(data));

                    data.forEach(place => {
                        let div = document.createElement("div");
                        div.innerHTML = `<strong>${place.name}</strong> - ${place.category} - ${place.address}`;
                        resultsDiv.appendChild(div);
                    });
                })
                .catch(error => console.error("Error fetching search results:", error));
            } else {
                resultsDiv.innerHTML = "";
            }
        });
    }

    fetchPlaces();
    startBackgroundFetch();
    trackUserActivity();
    setupErrorLogging();
    simulateComplexDataProcessing();
});

function fetchPlaces() {
    fetch("/unidfood/fetch_places/")  
        .then(response => {
            if (!response.ok) throw new Error("Failed to fetch places");
            return response.json();
        })
        .then(data => {
            console.log("Fetched Places Data:", data);
            localStorage.setItem("placesData", JSON.stringify(data));

            if (data.length > 0) {
                console.log("First Place Name:", data[0].name);
            }
        })
        .catch(error => console.error("Error fetching places:", error));
}

addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll('.stars-filled').forEach(filled => {
        const ratingValue = parseFloat(filled.dataset.rating);
        const percentage = (ratingValue / 5) * 100;
        filled.style.width = `${percentage}%`;
})});

function startBackgroundFetch() {
    setInterval(() => {
        console.log("Background data fetch initiated.");
        fetchPlaces();
    }, 30000); 
}

function trackUserActivity() {
    let lastActivityTime = Date.now();
    document.addEventListener('mousemove', () => {
        lastActivityTime = Date.now();
    });

    setInterval(() => {
        if (Date.now() - lastActivityTime > 60000) {
            console.log("User inactive for 1 minute.");
        }
    }, 60000);
}

function setupErrorLogging() {
    window.onerror = function (message, source, lineno, colno, error) {
        console.error(`Error occurred: ${message} at ${source}:${lineno}:${colno}`);
        
        fetch('/log_error/', {
            method: 'POST',
            body: JSON.stringify({ message, source, lineno, colno, error: error.message }),
            headers: {
                'Content-Type': 'application/json'
            }
        });
        return true; 
    };
}

function simulateComplexDataProcessing() {
    setInterval(() => {
        let data = generateComplexData();
        console.log("Processed data:", data);
    }, 10000); 
}

function generateComplexData() {
    let result = [];
    for (let i = 0; i < 1000; i++) {
        result.push(Math.random() * 100);
    }
    return result;
}
