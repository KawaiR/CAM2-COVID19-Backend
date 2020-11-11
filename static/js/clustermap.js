let map;
let markers = []

function initMap(){
    markerInfo = new google.maps.InfoWindow;
    
    var map = new google.maps.Map(document.getElementById('mapCanvas'),{
        zoom: 3,
        center:{
            lat: 41.876,
            lng: -87.624
        }
    });
    console.log("map initialized")
    d3.csv("camera_database.csv").then(function(data) {
        data.forEach(createMarker)
        var options ={
            imagePath: "img/m",
            styles:[{
                url:"img/m1.png",
                textSize:16,
                width: 54,
                height: 54,
                anchor:[0,0],
            },
            {
                url:"img/m2.png",
                textSize:16,
                width: 58,
                height: 58,
                anchor:[0,0],
            },
            {
                url:"img/m3.png",
                textSize:16,
                width: 68,
                height: 68,
                anchor:[0,0],
            },
            {
                url:"img/m4.png",
                textSize:16,
                width: 80,
                height: 80,
                anchor:[0,0],
            },
            {
                url:"img/m5.png",
                textSize:16,
                width: 93,
                height: 93,
                anchor:[0,0],
            },]
        }
        var markerCluster = new MarkerClusterer(map,markers,options)
    });
 
    function createMarker(camera) {
        var LatLng = {lat: parseFloat(camera.latitude), lng: parseFloat(camera.longitude)}
        var infocontent = 
        '<h5>Country:</h5>'+camera.country+
        '<h5>City:</h5>'+camera.city+
        '<h5>Latitude:</h5>'+camera.latitude+
        '<h5>Longitude:</h5>'+camera.longitude
        let marker = new google.maps.Marker({
          map: map,
          position: LatLng,
        });
        markers.push(marker)
        google.maps.event.addListener(marker, 'click', function() {
          markerInfo.setContent(infocontent);
          markerInfo.open(map, this);
        });
    }
}

