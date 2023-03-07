$(document).ready(function() {
	$("#save-button").click(function() {
		$.ajax({
			url: url_sauvegarder_polygone,
			type: "POST",
			dataType: "text",
			data: {
				jsonData: polygon,
				pseudo: pseudo,
				nom: $("#id_nom").val().toString(),
				plante:$("#id_plante").val().toString(),
				sol:$("#id_sol").val().toString(),
				date_deb_month: $("#id_date_deb_month").val().toString(),
				date_deb_day: $("#id_date_deb_day").val().toString(),
				date_deb_year: $("#id_date_deb_year").val().toString(),
				date_fin_month:$("#id_date_fin_month").val().toString(),
				date_fin_day:$("#id_date_fin_day").val().toString(),
				date_fin_year:$("#id_date_fin_year").val().toString(),
				csrfmiddlewaretoken: csrf_token
			},
			success : function(json) {
				alert(json);
			},
			error : function(xhr,errmsg,err) {
				alert("Error: "+xhr.status+": "+err );
			}
		});
	});
});
