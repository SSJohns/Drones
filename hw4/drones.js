var map;
var drones = [];
var jobs = [];

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {
            lat: 48.869317,
            lng: 2.30
        },
        zoom: 13,
    });
    var marker = new google.maps.Marker({
        position: {
            lat: 48.869317,
            lng: 2.30
        },
        // icon:"https://cdn1.iconfinder.com/data/icons/public-symbols-and-places/100/airport_arrival_flight_landing_aeroplane-128.png",
        map: map
    });

    main();
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
    console.log(mydata);
    for (i = 0; i < 5; i++) {
        var str = i.toString();
        str += 'efl';
        drones.push({
            str: [48.858093, 2.296604, i * 10 + 30],
            'battery': 25,
            'speed': 20
        });
        mark_drones(str, 48.858093, 2.296604);
    }
    for (i = 0; i < 5; i++) {
        var str = i.toString();
        str += 'ptn';
        drones.push({
            str: [48.846185, 2.346708, i * 10 + 30],
            'battery': 25,
            'speed': 20
        });
        mark_drones(str, 48.846185, 2.346708);
    }
    charge_stations();
}

function mark_drones(drone_id, lat, lng) {
    drone_markers = {};
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

function mark_boxes(drone_id, lat, lng) {
    drone_markers = {};
    console.log(lat, lng);
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
            icon: "http://www.basildon.gov.uk/media/page_icon/7/b/13AmpSocket.png",
            map: map
        });
        station[i].setPosition({
            lat: lat,
            lng: lng
        });
        i++;
    }
}
