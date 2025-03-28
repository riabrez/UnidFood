function loadGoogleMaps() {
    if (document.getElementById('googleMapsScript')) return; // Prevent duplicate loading

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
});

function fetchPlaces() {
    fetch("/fetch_places/")
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
