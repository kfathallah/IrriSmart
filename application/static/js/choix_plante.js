$("tr:not(#header)").click(function() {
	$(this).addClass("selected").siblings().removeClass("selected");
	document.getElementById("id_plante").value = $(this).find('td:first-child').html();
});

$('#creer').click(function() {
	window.location.href = creer_plante;
});
