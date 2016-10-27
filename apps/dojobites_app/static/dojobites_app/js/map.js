var map;
var infowindow;

function initMap() {
  var codingdojo = {lat: 47.609811, lng: -122.196526};

  map = new google.maps.Map(document.getElementById('map'), {
    center: codingdojo,
    zoom: 16
  });

  infowindow = new google.maps.InfoWindow();
  var service = new google.maps.places.PlacesService(map);
  service.nearbySearch({
    location: codingdojo,
    radius: 400,
    type: ['food']
  }, callback);
}

function callback(results, status) {
  if (status === google.maps.places.PlacesServiceStatus.OK) {
    console.log(results);
    for (var i = 0; i < results.length; i++) {
      createMarker(results[i]);
    }
  }
}

function createMarker(place) {
  var placeLoc = place.geometry.location;
  var marker = new google.maps.Marker({
    map: map,
    position: place.geometry.location
  });

  google.maps.event.addListener(marker, 'click', function() {
    infowindow.setContent(place.name + '<br>' + place.vicinity);
    $('#placeName').val(place.name);
    infowindow.open(map, this);
  });
}

$(document).ready(function() {

});
