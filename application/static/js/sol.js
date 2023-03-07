if (document.getElementById('return')) {
	$('#return').click(function() {
		window.location.href=retourner;
	});
	$('#id_sable').change(function() {
		$("#slider_sable").slider('value', $(this).val());
	});
	$('#id_argile').change(function() {
		$("#slider_argile").slider('value', $(this).val());
	});
	$('#id_limon').change(function() {
		$("#slider_limon").slider('value', $(this).val());
	});
}

var min=0, max=100, step=0.1;
$('.selector').slider(
	{animate: true, min: min, max: max, step: step},
	{change: function(event, ui) {
		$('#id_sable').val($("#slider_sable").slider("value"));
		$('#id_argile').val($("#slider_argile").slider("value"));
		$('#id_limon').val($("#slider_limon").slider("value"));
	}},
	{slide: function(event, ui) {
		$('#id_sable').val($("#slider_sable").slider("value"));
		$('#id_argile').val($("#slider_argile").slider("value"));
		$('#id_limon').val($("#slider_limon").slider("value"));
	}}
);

$("#slider_sable").slider('value', 0);
$("#slider_argile").slider('value', 0);
$("#slider_limon").slider('value', 0);

function refreshSliders(slidermainin) {
	var sable = $("#slider_sable").slider("option", "value"),
	argile = $("#slider_argile").slider("option", "value"),
	limon = $("#slider_limon").slider("option", "value"),
	valuechange = (sable + argile + limon) - 100,
	valuemain = 0,
	valueother1 = 0,
	valueother2 = 0;
	if(slidermainin == 1) {
		slidermain = "#slider_sable";
		sliderother1 = "#slider_argile";
		sliderother2 = "#slider_limon";
		valuemain = sable;
		valueother1 = argile;
		valueother2 = limon;
	} else if (slidermainin == 2) {
		slidermain = "#slider_argile";
		sliderother1 = "#slider_limon";
		sliderother2 = "#slider_limon";
		valuemain = argile;
		valueother1 = limon;
		valueother2 = limon;
	} else if (slidermainin == 3) {
		slidermain = "#slider_limon";
		sliderother1 = "#slider_sable";
		sliderother2 = "#slider_argile";
		valuemain = limon;
		valueother1 = sable;
		valueother2 = argile;
	}
	if (valueother1 === 0 || valueother2 === 0) {
		if (valueother1 === 0) {
			if (valuechange <= 0) {
				$(sliderother1).slider('value', valueother1-(valuechange/2));
				$(sliderother2).slider('value', valueother2-(valuechange/2));
			} else {
				$(sliderother2).slider('value', valueother2-valuechange);
			}
		} else {
			if (valuechange <= 0) {
				$(sliderother1).slider('value', valueother1-(valuechange/2));
				$(sliderother2).slider('value', valueother2-(valuechange/2));
			} else {
				$(sliderother1).slider('value', valueother1-valuechange);
			} 
		}
	} else {
		$(sliderother1).slider('value', valueother1-(valuechange/2));
		$(sliderother2).slider('value', valueother2-(valuechange/2));
	}
}

var bindSliders = function(selector, value) {
	$(selector).bind("slidechange slide", function(event, ui) {
		event.originalEvent && (event.originalEvent.type == 'mousemove' || event.originalEvent.type == 'mouseup') && refreshSliders(value);
	});
};

bindSliders("#slider_sable", 1);
bindSliders("#slider_argile", 2);
bindSliders("#slider_limon", 3);
