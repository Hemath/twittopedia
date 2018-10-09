$(document).ready(function(){

	$('#login_form').on('submit', function(event) {

		$.ajax({
			data : {
				email : $('#Login_Email').val(),
				password : $('#Login_Password').val()
			},

			type : 'POST',
			url : '/login_process',

			success: function(response){
				if (response)
				{
					var res = JSON.parse(response);

					if (res.response.login == "wrong_password")
					{
						swal({
							title:"Oops !",
							text:"The password you entered seems like to be Wrong! Check it!",
							icon:"warning"
						});
					}

					else if (res.response.login == "no_user")
					{
						swal({
							title:"Oops !",
							text:"Seems like, No Such User !",
							icon:"error"
						});
					}

					else if (res.response.login == "success")
					{
						window.location.href = "dashboard";
					}
				}
			}
		})

		event.preventDefault();

	});


	$('#register_form').on('submit', function(event) {

		$.ajax({
			data : {
				first_name : $('#Register_FirstName').val(),
				last_name : $('#Register_LastName').val(),
				email : $('#Register_Email').val(),
				password : $('#Register_Password').val(),
				confirm_password : $('#Register_ConfirmPassword').val(),
			},

			type : 'POST',
			url : '/register_process',

			success: function(response){
				var res = JSON.parse(response);

				if (res.response.status == "OK")
				{
					swal({
						title:"Success!",
						text:"Yeah! Your account has been created!",
						icon:"success"
					});

					$("#exampleModalCenter2").modal('toggle');
				}
				else if (res.response.already == "OK")
				{
					swal({
						title:"Sorry!",
						text:"This email is already is registered!",
						icon:"error"
					});
				}
				else
				{
					if (res.response.first_name == 1)
					{
						$("#first_name_error").html('<span class="custom-alert alert alert-danger">First Name is Required!</span>');
						$("#email_error").html('');
						$("#password_error").html('');
						$("#confirm_password_error").html('');
					}

					else if (res.response.email == 1)
					{
						$("#email_error").html('<span class="custom-alert alert alert-danger">Email is Required!</span>');
						$("#first_name_error").html('');
						$("#password_error").html('');
						$("#confirm_password_error").html('');
					}

					else if (res.response.password == 1)
					{
						$("#password_error").html('<span class="custom-alert alert alert-danger">Passowrd is Required!</span>');
						$("#first_name_error").html('');
						$("#email_error").html('');
						$("#confirm_password_error").html('');
					}

					else if (res.response.confirm_password == 1)
					{
						$("#confirm_password_error").html('<span class="custom-alert alert alert-danger">This password is required for Confirmation!</span>');
						$("#first_name_error").html('');
						$("#email_error").html('');
						$("#password_error").html('');
					}

					else if (res.response.not_match)
					{
						$("#confirm_password_error").html('<span class="custom-alert alert alert-danger">Passowrds don\'t match!</span>');
						$("#first_name_error").html('');
						$("#email_error").html('');
						$("#password_error").html('');
					}

					else
					{
						$("#first_name_error").html('');
						$("#email_error").html('');
						$("#password_error").html('');
						$("#confirm_password_error").html('');
					}
				}
			}

		})


		event.preventDefault();

	});

});