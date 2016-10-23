drone_markers = {};
drone_markers[drone_id] = new google.maps.Marker({
	position: {lat: lat, lng: lng},
	map: map
}); // code to create the marker the first time - lat,lng are coordinates to place marker at, map is the map to show it on
drone_markers[drone_id].setPosition({lat: lat, lng: lng}); // code to move the marker to a different position (at lat,lng)
