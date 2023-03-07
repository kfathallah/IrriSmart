var nom = {
    vent: 'vent',
    humsol: 'humidite de sol',
    tmphum: 'temperature et humidite',
    radiation: 'radiation solaire'
},
selectedMarker, drawingManager, map, markers = [];

function getProprietes(marker) {
    var dictionnaire = {},
    nb_false = 0;
    for (key in icons) {
        if (marker[key] == false) {nb_false++;}
        dictionnaire[nom[key]] = marker[key];
    }
    if (nb_false == Object.keys(icons).length) {return null;}
    return dictionnaire;
}

function hover(element) {
    for (key in icons) {
        document.getElementById(key).checked = element[key];
    }
    selectedMarker = element;
    document.getElementById('legend').style.visibility = 'visible';
}

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 13,
        center: {lat: lat, lng: lng},
        streetViewControl: false
    });
    drawingManager = new google.maps.drawing.DrawingManager({
        drawingControlOptions: {
            position: google.maps.ControlPosition.TOP_CENTER,
            drawingModes: [google.maps.drawing.OverlayType.MARKER]
        },
        markerOptions: {
            icon: markerType['normal'],
            draggable: true,
            animation: google.maps.Animation.DROP
        },
        map: map
    });
    drawingManager.setMap(map);
    google.maps.event.addListener(drawingManager, 'markercomplete', function(marker) {
        marker.id = markers.length;
        for (key in icons) {
            marker[key] = false;
        }
        marker.addListener('click', function() {hover(this);});
        marker.addListener('mouseup', function() {hover(this);});
        selectedMarker = marker;
        markers.push(marker);
    });
    var legend = document.getElementById('legend');
    for (var key in icons) {
        var icon = icons[key],
        div = document.createElement('div');
        div.innerHTML = '<input type="checkbox" id="' + key + '" name="liste[]"><img src="' + icon + '">' + nom[key] + '</input>';
        legend.appendChild(div);
        google.maps.event.addDomListener(document.getElementById(key), 'change', function() {
            selectedMarker[this.id] = this.checked;
            if ($('[name="liste[]"]:checked').length != 0) {selectedMarker.setIcon(markerType['valide']);}
            else {selectedMarker.setIcon(markerType['erreur']);}
        });
    }
    map.controls[google.maps.ControlPosition.RIGHT_TOP].push(legend);
    google.maps.Map.prototype.getGeoJson = function(callback) {
        var geo = {
            type: "FeatureCollection",
            features: []
        };
        for (var i in markers) {
            var _properties = getProprietes(markers[i]),
            feature = {
                'type': 'Feature',
                'properties': _properties,
                'geometry': {
                    'type': 'POINT',
                    'coordinates': [[[markers[i].getPosition().lat(), markers[i].getPosition().lng()]]]
                }
            };
            if (_properties == null) {
                markers[i].setIcon(markerType['erreur']);
            } else {geo.features.push(feature);}
        }
        if (typeof callback === 'function') {
            callback(geo);
        }
        return geo;
    }
    google.maps.event.addDomListener(document.getElementById('supprimer'), 'click', function() {
        if (selectedMarker) {
            markers.splice(selectedMarker.id, 1);
            selectedMarker.setMap(null);
            document.getElementById('legend').style.visibility = 'hidden';
        }
    });
    google.maps.event.addDomListener(document.getElementById('sauvegarder'), 'click', function() {
        map.getGeoJson(function(geo) {
            if (geo.features.length == markers.length && markers.length != 0) {
                $.ajax({
                    url: url,
                    type: "POST",
                    data: {
                        geojson: JSON.stringify(geo),
                        csrfmiddlewaretoken: csrf_token
                    },
                    success: function(reponse) {window.location.href = reponse;},
                    error: function(xhr, errmsg, err) {alert("Error: " + xhr.status + ": " + err);}
                });
            }
            else if (geo.features.length != markers.length) {alert('Veuillez affecter le type de chaque noeud!');}
            else {alert('Placer vos noeuds!');}
        });
    });
    map.data.addGeoJson(parcelles);
}
