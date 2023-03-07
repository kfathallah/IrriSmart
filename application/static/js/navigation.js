$(document).ready(function() {
	$('#close').click(function() {
		$('#dataCompte').css({"-webkit-transform":"translate(310px)","transform":"translate(310px)"});
	});
	$('#ouvrirCompte').click(function() {
		$('#dataCompte').css({"-webkit-transform":"translate(0px)","transform":"translate(0px)"});
	});
});
