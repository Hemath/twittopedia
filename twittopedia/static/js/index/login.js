$(document).ready(function(){


	$('#login_form').on('submit', function(event) {

		$.ajax({
			data : {
				email : $('#emailInputLogin').val(),
				password : $('#passwordLogin').val()
			},

			type : 'POST',
			url : '/loginCheck'
		})

		.done(function(data) {
			if (data.login == "NO_SUCH_USER"){
				$('#errorAlertLogin').text("No Such User").show();
				$('#successAlertLogin').hide();
			}
			else if(data.login == "TRUE")
			{
				$('#successAlertLogin').text("Logged In!").show();
				$('#errorAlertLogin').hide();
			}
			else if(data.login == "password")
			{
				$('#errorAlertLogin').text("Wrong Password!").show();
				$('#successAlertLogin').hide();
			}
			else
			{
				$('#successAlertLogin').show();
				$('#errorAlertLogin').show();
			}
		})

		event.preventDefault();

	});


});