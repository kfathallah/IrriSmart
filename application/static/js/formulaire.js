$(document).ready(function() {
	$("#annuler").click(function() {
		window.location.href = '/application/';
	});
	if (document.getElementById('mdp')) {
		$("#mdp").click(function() {
			window.location.href = changer_mot_de_passe;
		});
	}
	if (document.getElementById('profile')) {
		$("#profile").click(function() {
			window.location.href = changer_photo;
		});
	}
	if (document.getElementById('supprimer_photo')) {
		$("#supprimer_photo").click(function() {
			$.ajax({
				url: supprimer_photo,
				type: "POST",
				dataType: "text",
				data: {
					pseudo: pseudo,
					csrfmiddlewaretoken: csrf_token
				},
				success: function(json) {
					$("#photo_profile").remove();
					window.location.href = '/application/profile/photo/';
				}
			});
		});
	}
});
