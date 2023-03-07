var drawingManager;
var selectedShape;
var colors = ['#1E90FF', '#FF1493', '#32CD32', '#FF8C00', '#4B0082'];
var selectedColor;
var colorButtons = {};
var map;
var shapes = [];

function clearSelection() {
    if (selectedShape) {
        selectedShape.setEditable(false);
        selectedShape = null;
    }
}

function setSelection(shape) {
    clearSelection();
    selectedShape = shape;
    shape.setEditable(true);
    selectColor(shape.get('fillColor') || shape.get('strokeColor'));
}

function deleteSelectedShape() {
    if (selectedShape) {
        shapes.splice(selectedShape.id, 1);
        selectedShape.setMap(null);
    }
}

function importerPolygones() {
    var allVals = [];
    $.each($("input[name='checkbox']:checked"), function() {
        allVals.push($(this).val());
    });
    $.ajax({
        url: url_importer_polygone,
        type: "POST",
        data: {
            id: allVals,
            csrfmiddlewaretoken: csrf_token
        },
        success: function(json) {
            json = JSON.parse(json);
            map.data.addGeoJson(json);
        },
        error: function(xhr, errmsg, err) {
            alert("Error: " + xhr.status + ": " + err);
        }
    });
}

function selectColor(color) {
    selectedColor = color;
    for (var i = 0; i < colors.length; ++i) {
        var currColor = colors[i];
        colorButtons[currColor].style.border = currColor == color ? '2px solid #789' : '2px solid #fff';
    }

    var polylineOptions = drawingManager.get('polylineOptions');
    polylineOptions.strokeColor = color;
    drawingManager.set('polylineOptions', polylineOptions);

    var rectangleOptions = drawingManager.get('rectangleOptions');
    rectangleOptions.fillColor = color;
    drawingManager.set('rectangleOptions', rectangleOptions);

    var circleOptions = drawingManager.get('circleOptions');
    circleOptions.fillColor = color;
    drawingManager.set('circleOptions', circleOptions);

    var polygonOptions = drawingManager.get('polygonOptions');
    polygonOptions.fillColor = color;
    drawingManager.set('polygonOptions', polygonOptions);
}

function setSelectedShapeColor(color) {
    if (selectedShape) {
        if (selectedShape.type == google.maps.drawing.OverlayType.POLYLINE) {
            selectedShape.set('strokeColor', color);
        } else {
            selectedShape.set('fillColor', color);
        }
    }
}

function makeColorButton(color) {
    var button = document.createElement('span');
    button.className = 'color-button';
    button.style.backgroundColor = color;
    google.maps.event.addDomListener(button, 'click', function() {
        selectColor(color);
        setSelectedShapeColor(color);
    });

    return button;
}

function buildColorPalette() {
    var colorPalette = document.getElementById('color-palette');
    for (var i = 0; i < colors.length; ++i) {
        var currColor = colors[i];
        var colorButton = makeColorButton(currColor);
        colorPalette.appendChild(colorButton);
        colorButtons[currColor] = colorButton;
    }
    selectColor(colors[0]);
}

function initialize() {
    var input = document.getElementById('searchTextField');
    var autocomplete = new google.maps.places.SearchBox(input);
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 15,
        center: new google.maps.LatLng(latitude, longitude),
        mapTypeId: google.maps.MapTypeId.HYBRID,
        disableDefaultUI: true,
        zoomControl: true
    });
    map.controls[google.maps.ControlPosition.TOP_RIGHT].push(input);
    map.addListener('bounds_changed', function() {
        autocomplete.setBounds(map.getBounds());
    });
    var markers = [];
    autocomplete.addListener('places_changed', function() {
        var places = autocomplete.getPlaces();
        if (places.length == 0) {
            return;
        }
        markers.forEach(function(marker) {
            marker.setMap(null);
        });
        markers = [];
        var bounds = new google.maps.LatLngBounds();
        places.forEach(function(place) {
            var icon = {
                url: place.icon,
                size: new google.maps.Size(71, 71),
                origin: new google.maps.Point(0, 0),
                anchor: new google.maps.Point(17, 34),
                scaledSize: new google.maps.Size(25, 25)
            };
            markers.push(new google.maps.Marker({
                map: map,
                icon: icon,
                title: place.name,
                position: place.geometry.location
            }));
            if (place.geometry.viewport) {
                bounds.union(place.geometry.viewport);
            } else {
                bounds.extend(place.geometry.location);
            }
        });
        map.fitBounds(bounds);
    });
    var polyOptions = {
        strokeWeight: 0,
        fillOpacity: 0.45,
        editable: true
    };
    drawingManager = new google.maps.drawing.DrawingManager({
        drawingControlOptions: {
            drawingModes: [
                google.maps.drawing.OverlayType.POLYGON
            ]
        },
        markerOptions: {
            draggable: true
        },
        polylineOptions: {
            editable: true
        },
        rectangleOptions: polyOptions,
        circleOptions: polyOptions,
        polygonOptions: polyOptions,
        map: map
    });
    google.maps.event.addListener(drawingManager, 'overlaycomplete', function(e) {
var zooom = map.getZoom();
	if (zooom >17 || zooom< 15 ){
e.overlay.setMap(null);
alert('Impossible de déssiner sur ce level de zoom '+zooom+', Zoomez ou Dézoomez entre 15 et 17 ');
}
        if (e.type != google.maps.drawing.OverlayType.MARKER) {
            drawingManager.setDrawingMode(null);
            var newShape = e.overlay;
            newShape.type = e.type;
            newShape.id = shapes.length;
            shapes.push(newShape);
            google.maps.event.addListener(newShape, 'click', showArrays);
            infoWindow = new google.maps.InfoWindow();
            setSelection(newShape);
            google.maps.event.addListener(newShape.getPath(), 'set_at', processVertex);
            google.maps.event.addListener(newShape.getPath(), 'insert_at', processVertex);
        }
    });

    function showArrays(event) {
var zooom = map.getZoom();
        setSelection(this);
        var vertices = this.getPath();
        var contentString = '<b>Polygon suivant ' + this.id  +': '+zooom+'</b><br>' +
            'Clicked location: <br>' + event.latLng.lat() + ',' + event.latLng.lng();
        for (var i = 0; i < vertices.getLength(); i++) {
            var xy = vertices.getAt(i);
            contentString += '<br><br>' + 'Coordinate ' + i + ':<br>' + xy.lat() + ',' + xy.lng();
        }
        infoWindow.setContent(contentString);
        infoWindow.setPosition(event.latLng);
        infoWindow.open(map);
    }

    function processVertex(e) {
        for (var i = 0; i < shapes.length; i++) {
            if (shapes[i].getPath() == this) {
                console.log('shape: ' + i + ', vertex: ' + e);
            }
        }
    }

    google.maps.event.addListener(drawingManager, 'drawingmode_changed', clearSelection);
    google.maps.event.addListener(map, 'click', clearSelection);
    buildColorPalette();
    google.maps.event.addDomListener(document.getElementById('supprimer'), 'click', deleteSelectedShape);
    google.maps.event.addDomListener(document.getElementById('suivant'), 'click', function() {
        map.getGeoJson(function(geo) {
            if (geo['features'].length!=0) {
                $.ajax({
                    url: url_sauvegarder_polygone,
                    type: "POST",
                    data: {
                        geojson: JSON.stringify(geo),
                        csrfmiddlewaretoken: csrf_token
                    },
                    success: function(reponse) {
                        window.location.href = reponse;
                    },
                    error: function(xhr, errmsg, err) {
                        alert("Error: " + xhr.status + ": " + err);
                    }
                });
            } else {alert('Selectionner votre parcelle!')}
        });
    });
    btnImporter=document.getElementById('importer-button');
    if (btnImporter) {google.maps.event.addDomListener(btnImporter, 'click', importerPolygones);}
    google.maps.Map.prototype.getGeoJson = function(callback) {
        var geo = {
                "type": "FeatureCollection",
                "features": []
            },
            fxShapes = function(vertices) {
                var that = [];
                for (var i = 0; i < vertices.getLength(); ++i) {
                    that.push([vertices.getAt(i).lng(), vertices.getAt(i).lat()]);
                }
                if (that[0] !== that[that.length - 1]) {
                    that.push([that[0][0], that[0][1]]);
                }
                return that;
            },
            fx = function(g, t) {

                var that = [],
                    arr,
                    f = {
                        MultiLineString: 'LineString',
                        LineString: 'Point',
                        MultiPolygon: 'Polygon',
                        Polygon: 'LinearRing',
                        LinearRing: 'Point',
                        MultiPoint: 'Point'
                    };

                switch (t) {
                    case 'Point':
                        g = (g.get) ? g.get() : g;
                        return ([g.lng(), g.lat()]);
                        break;
                    default:
                        arr = g.getArray();
                        for (var i = 0; i < arr.length; ++i) {
                            that.push(fx(arr[i], f[t]));
                        }
                        if (t == 'LinearRing' &&
                            that[0] !== that[that.length - 1]) {
                            that.push([that[0][0], that[0][1]]);
                        }
                        return that;
                }
            };

        this.data.forEach(function(feature) {
            var _feature = {
                type: 'Feature',
                properties: {}
            }
            _id = feature.getId(),
                _geometry = feature.getGeometry(),
                _type = _geometry.getType(),
                _coordinates = fx(_geometry, _type);

            _feature.geometry = {
                type: _type,
                coordinates: _coordinates
            };
            if (typeof _id === 'string') {
                _feature.id = _id;
            }

            geo.features.push(_feature);
            feature.forEachProperty(function(v, k) {
                _feature.properties[k] = v;
            });
        });
        shapes.forEach(function(shape) {
            var _feature = {
                type: 'Feature',
                properties: {}
            }
            _geometry = shape.getPath(),
                _type = shape.type,
                _coordinates = fxShapes(_geometry, _type);

            _feature.geometry = {
                type: _type,
                coordinates: [_coordinates]
            };
            if (typeof _id === 'string') {
                _feature.id = _id;
            }
            geo.features.push(_feature);
        });
        if (typeof callback === 'function') {
            callback(geo);
        }
        return geo;
    }
}
