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

    const input = document.getElementById("searchBox");
    if (input) {
        const searchBox = new google.maps.places.SearchBox(input);
        map.addListener("bounds_changed", () => searchBox.setBounds(map.getBounds()));

        let markers = [];
        searchBox.addListener("places_changed", () => {
            const places = searchBox.getPlaces();
            if (!places.length) return;

            markers.forEach(marker => marker.setMap(null)); 
            markers = [];

            const bounds = new google.maps.LatLngBounds();
            places.forEach(place => {
                if (!place.geometry?.location) return;

                const marker = new google.maps.Marker({
                    map,
                    title: place.name,
                    position: place.geometry.location
                });
                markers.push(marker);
                bounds.extend(place.geometry.viewport || place.geometry.location);
            });
            map.fitBounds(bounds);
        });
    }
}

document.addEventListener("DOMContentLoaded", () => {
    if (document.getElementById("map")) loadGoogleMaps();
});

document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("search");
    const resultsDiv = document.getElementById("results");

    if (!searchInput || !resultsDiv) return;

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
});


function fetchPlaces() {
    fetch("/fetch_places/")  
        .then(response => response.json())  
        .then(data => {
            console.log("Fetched Places Data:", data);  

            localStorage.setItem("placesData", JSON.stringify(data));
            
            if (data.length > 0) {
                console.log("First Place Name:", data[0].name);
            }
        })
        .catch(error => console.error("Error fetching places:", error));
}

fetchPlaces();

