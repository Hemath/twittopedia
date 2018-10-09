$(document).ready(function(){


	$('#register_form').on('submit', function(event) {

		$.ajax({
			data : {
				first_name : $('#FirstName').val(),
				last_name : $('#LastName').val(),
				email : $('#Email').val(),
				password : $('#Password').val(),
				confirm_password : $('#ConfirmPassword').val(),
			},

			type : 'POST',
			url : '/register_process'
		})

		.done(function(data) {
			if (data.error){
				$('#errorAlert').text(data.error).show();
				$('#successAlert').hide();
			}
		})

		event.preventDefault();

	});


});