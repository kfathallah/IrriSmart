var infowindow, contentString, proprietes, map,
nomProprietes = {
	'altitude': 'Altitude',
	'pression': 'Pression',
	'temperature': 'Temperature',
	'vent': 'Vent',
	'humidite': 'Humidite',
	'humidite_sol': 'humidite de sol',
	'radiation': 'Radiation solaire',
	'true': 'Disponible',
	'false': "Indisponible"
};

function setInfowindow(marker) {
	proprietes = "";
	var valuer;
	marker.forEachProperty(function(v, k) {if (k != 'projet' && k != 'pk') {
		if (v == true || v == false) {valeur = nomProprietes[v];}
		else {valeur = v; v = '';}
		proprietes += '<p class="nom">'+nomProprietes[k]+'</p><p class="valeur '+v+'">'+valeur+'</p></br>';
	}});
	contentString = '<div id="content"><div id="siteNotice"></div>' +
	'<h1 id="firstHeading" class="firstHeading">' + $('#' + marker.getProperty('pk')).html() + '</h1><hr/>' +
	'<div id="bodyContent">' + proprietes + '</div></div>';
	infowindow.setContent(contentString);
}

function initializer() {
	map = new google.maps.Map(document.getElementById('map'), {
		zoom: 10,
		center: new google.maps.LatLng(latitude, longitude),
		mapTypeId: google.maps.MapTypeId.HYBRID,
		disableDefaultUI: true,
		zoomControl: true
	});
	map.data.addGeoJson(noeud);
	map.data.addGeoJson(parcelle);
	map.data.setStyle({
		fillColor: 'green',
		strokeWeight: 1
	});
	infowindow = new google.maps.InfoWindow({});
	map.data.addListener('click', function(event) {
		var objet = event.feature,
		geometry = objet.getGeometry();
		if (geometry.getType() == 'Point') {
			var latLng = geometry.get();
			if (infowindow) {infowindow.close();}
			setInfowindow(objet);
			infowindow.setPosition(latLng);
			infowindow.open(map);
		}
	});
}

function getData(titres, donnees) {
	return {
		"type": "serial",
		"categoryField": "date",
		"dataDateFormat": "YYYY-MM-DD HH:NN:SS",
		"categoryAxis": {
			"minPeriod": "ss",
			"parseDates": true
		},
		"chartCursor": {
			"enabled": true,
			"categoryBalloonDateFormat": "JJ:NN:SS"
		},
		"chartScrollbar": {
			"enabled": true
		},
		"trendLines": [],
		"graphs": graphes,
		"guides": [],
		"valueAxes": [
			{
				"id": "ValueAxis-1",
				"title": "Axis title"
			}
		],
		"allLabels": [],
		"balloon": {},
		"legend": {
			"enabled": true,
			"useGraphSettings": true
		},
		"titles": [
			{
				"id": "Title-1",
				"size": 15,
				"text": titres
			}
		],
		"dataProvider": donnees
	
	}
}
