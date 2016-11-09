var map;
var drones = [];
var jobs = [];
drone_markers = {};
var delay = 0;
var j = 0;

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function sleepFor( sleepDuration ){
    var now = new Date().getTime();
    while(new Date().getTime() < now + sleepDuration){ /* do nothing */ }
}

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {
            lat: ((48.869317 + 48.839458)/2),
            lng: ((2.399188 + 2.278953)/2)
        },
        zoom: 13,
    });
    main();
    setInterval(periodicPan, 1000);
}

function isEmpty(obj) {
   for (var x in obj) { return false; }
   return true;
}

function animateMarker(marker, startPos, coords, km_h)
{
    var target = 0;
    var km_h = km_h || 50;
    coords.push([startPos[0], startPos[1]]);

    function goToPoint()
    {
        var lat = marker.position.lat();
        var lng = marker.position.lng();
        var step = (km_h * 1000 * delay) / 3600000; // in meters

        var dest = new google.maps.LatLng(
        coords[target][0], coords[target][1]);

        var distance =
        google.maps.geometry.spherical.computeDistanceBetween(
        dest, marker.position); // in meters

        var numStep = distance / step;
        var i = 0;
        var deltaLat = (coords[target][0] - lat) / numStep;
        var deltaLng = (coords[target][1] - lng) / numStep;

        function moveMarker()
        {
            lat += deltaLat;
            lng += deltaLng;
            i += step;

            if (i < distance)
            {
                marker.setPosition(new google.maps.LatLng(lat, lng));
                setTimeout(moveMarker, delay);
            }
            else
            {   marker.setPosition(dest);
                target++;
                if (target == coords.length){ target = 0; }

                setTimeout(goToPoint, delay);
            }
        }
        moveMarker();
    }
    goToPoint();
}

function periodicPan(){
    if ( isEmpty(batch[j]) ){
        j++;
        if ( j > batch.length ){
            clearInterval();
        }
    }
    for (point in batch[j] ){
        console.log(batch[j][point])
        move_drones( parseInt(batch[j][point]["droneID"]), parseFloat(batch[j][point]["lat"]), parseFloat(batch[j][point]["lon"]));
        delete batch[j][point];
    }

}

function main() {
    var mydata = JSON.parse(data);

    for (var obj in mydata) {
        jobs.push({
            'job': mydata[obj]['droneID'],
            'lat': parseFloat(mydata[obj]['lat']),
            'lng': parseFloat(mydata[obj]['lon'])
        })
        mark_boxes(mydata[obj]['droneID'], parseFloat(mydata[obj]['lat']), parseFloat(mydata[obj]['lon']));
    }
    // console.log(mydata);
    for (i = 0; i < 5; i++) {
        var str = i.toString();
        drones.push({
            'id':str,
            'loc': [48.858093, 2.296604, i * 10 + 30],
            'battery': 25,
            'speed': 20
        });
        mark_drones(str, 48.858093, 2.296604);
    }
    for (i = 5; i < 10; i++) {
        var str = i.toString();
        drones.push({
            'id': str,
            'loc': [48.846185, 2.346708, i * 10 + 30],
            'battery': 25,
            'speed': 20
        });
        mark_drones(str, 48.846185, 2.346708);
    }
    charge_stations();

    // console.log(drone_markers);

}

function draw_drones(points){
    for (point in points){
        console.log(points[point]);
        // Do something after the sleep!
        move_drones( parseInt(points[point]['droneID']), parseFloat(points[point]['lat']), parseFloat(points[point]['lon']));

    }
}
function mark_drones(drone_id, lat, lng) {
    // console.log(lat, lng);
    drone_markers[drone_id] = new google.maps.Marker({
        position: {
            lat: lat,
            lng: lng
        },
        map: map
    }); // code to create the marker the first time - lat,lng are coordinates to place marker at, map is the map to show it on
    drone_markers[drone_id].setPosition({
        lat: lat,
        lng: lng
    }); // code to move the marker to a different position (at lat,lng)

    // Add circle overlay and bind to marker
    var circle = new google.maps.Circle({
        map: map,
        radius: 10, // 10 miles in metres
        fillColor: '#ff0000'
    });
    circle.bindTo('center', drone_markers[drone_id], 'position');
}

function move_drones(drone_id, lat, lng, str_lat, str_lon) {
    drone_markers[drone_id].setPosition({
        lat: lat,
        lng: lng
    }); // code to move the marker to a different position (at lat,lng)
    // speed = 200 // km/hr
    // var str_lat = drone_markers[drone_id].getPosition().lat();
    // var str_lng = drone_markers[drone_id].getPosition().lng();
    // google.maps.event.addListenerOnce(map, 'idle', function()
    // {
    //     animateMarker(drone_markers[drone_id],
    //         [ str_lat, str_lon ],
    //         [
    //         // The coordinates of each point you want the marker to go to.
    //         // You don't need to specify the starting position again.
    //         [lat, lng]
    //     ], speed);
    // });
}

function mark_boxes(drone_id, lat, lng) {
    drone_markers = {};
    // console.log(lat, lng);
    drone_markers[drone_id] = new google.maps.Marker({
        position: {
            lat: lat,
            lng: lng
        },
        icon: "http://download.seaicons.com/icons/umut-pulat/tulliana-2/16/k-black-box-icon.png",
        map: map
    }); // code to create the marker the first time - lat,lng are coordinates to place marker at, map is the map to show it on
    drone_markers[drone_id].setPosition({
        lat: lat,
        lng: lng
    }); // code to move the marker to a different position (at lat,lng)
}


function charge_stations() {
    recharge_stations = {
        48.864446: 2.325283,
        48.858093: 2.296604,
        48.846185: 2.346708
    };
    stations = {};
    var i = 0;
    var station = {};
    for (var key in recharge_stations) {
        lat = parseFloat(key, 10);
        lng = parseFloat(recharge_stations[key], 10);
        station[i] = new google.maps.Marker({
            position: {
                lat: lat,
                lng: lng
            },
            icon: "http://icdn.pro/images/en/b/a/battery-charge-icone-6159-48.png",
            map: map
        });
        station[i].setPosition({
            lat: lat,
            lng: lng
        });
        i++;
    }
}
