function initialize() {
var element = document.getElementById("map");
var uluru = {lat: -25.363, lng: 131.044};

	var map = new google.maps.Map(element, {
		center: uluru,
		zoom: 3,
		mapTypeId: "OSM",
		mapTypeControl: false,
		streetViewControl: false
	});

	 var marker = new google.maps.Marker({
	  position: uluru,
	  map: map
	});

	//Define OSM map type pointing at the OpenStreetMap tile server
	map.mapTypes.set("OSM", new google.maps.ImageMapType({
		getTileUrl: function(coord, zoom) {
			// "Wrap" x (logitude) at 180th meridian properly
			// NB: Don't touch coord.x because coord param is by reference, and changing its x property breakes something in Google's lib 
			var tilesPerGlobe = 1 << zoom;
			var x = coord.x % tilesPerGlobe;
			if (x < 0) {
				x = tilesPerGlobe+x;
			}
			// Wrap y (latitude) in a like manner if you want to enable vertical infinite scroll

			return "http://tile.openstreetmap.org/" + zoom + "/" + x + "/" + coord.y + ".png";
		},
		tileSize: new google.maps.Size(256, 256),
		name: "OpenStreetMap",
		maxZoom: 18
	}));
}