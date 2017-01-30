// main var
var map;
var markers=[];

// main init function
function initialize() {
//openstreetmap

	var element = document.getElementById("map");
	var uluru = {lat: -25.363, lng: 131.044};

	var map = new google.maps.Map(element,  myOptions);
	
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


//listeners


	
	google.maps.event.addListener(map, 'dragend', function() {
		center = gmap_getCenter();
		qtWidget.mapMoved(center.lat(), center.lng());
	});
	google.maps.event.addListener(map, 'click', function(ev) {
		qtWidget.mapClicked(ev.latLng.lat(), ev.latLng.lng());
	});
	google.maps.event.addListener(map, 'rightclick', function(ev) {
		qtWidget.mapRightClicked(ev.latLng.lat(), ev.latLng.lng());
	});
	google.maps.event.addListener(map, 'dblclick', function(ev) {
		qtWidget.mapDoubleClicked(ev.latLng.lat(), ev.latLng.lng());
	});
}

// custom functions
function gmap_setCenter(lat, lng)
{
    map.setCenter(new google.maps.LatLng(lat, lng));
}

function gmap_getCenter()
{
	return map.getCenter();
}

function gmap_setZoom(zoom)
{
    map.setZoom(zoom);
}

function gmap_addMarker(key, latitude, longitude, parameters)
{

	if (key in markers) {
		gmap_deleteMarker(key);
	}

	var coords = new google.maps.LatLng(latitude, longitude);
	parameters['map'] = map
	parameters['position'] = coords;

	var marker = new google.maps.Marker(parameters);
	google.maps.event.addListener(marker, 'dragend', function() {
		qtWidget.markerMoved(key, marker.position.lat(), marker.position.lng())
	});
	google.maps.event.addListener(marker, 'click', function() {
		qtWidget.markerClicked(key, marker.position.lat(), marker.position.lng())
	});
	google.maps.event.addListener(marker, 'dblclick', function() {
		qtWidget.markerDoubleClicked(key, marker.position.lat(), marker.position.lng())
	});
	google.maps.event.addListener(marker, 'rightclick', function() {
		qtWidget.markerRightClicked(key, marker.position.lat(), marker.position.lng())
	});

	markers[key] = marker;
	return key;
}

function gmap_moveMarker(key, latitude, longitude)
{
	var coords = new google.maps.LatLng(latitude, longitude);
	markers[key].setPosition(coords);
}

function gmap_deleteMarker(key)
{
	markers[key].setMap(null);
	delete markers[key]
}

function gmap_changeMarker(key, extras)
{
	if (!(key in markers)) {
		return
	}
	markers[key].setOptions(extras);
}


