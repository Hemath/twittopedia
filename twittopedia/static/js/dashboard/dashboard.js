$(document).ready(function()
{
	$('#fetch').on('click', function(event){

		swal("How many Tweets?",
		{
			content:"input",
		})
		.then((value) => {
			swal("Wait!", "We will notify if the analyzation is finished", "info");

			$.ajax({
			data : {
				count:value
			},

			type : 'POST',
			url : '/fetch',

			success: function(response){
				if (response)
				{
					var res = JSON.parse(response);

					if (res.response == "OK")
					{
						swal("Finished!","Fetching has been finished!");
					}
					else
					{
						console.log(response);
					}
				}
			}
		})
		});
	});

	$('#update').on('click', function(event){

		$.ajax({
			data : {
			},

			type : 'GET',
			url : '/update',

			success: function(response){
				if (response)
				{
					var res = JSON.parse(response);

					if (res.response == "OK")
					{
						swal("Finished!","Data has been Updated!");
					}
				}
			}
		})

	});

	$('#analyze').on('click', function(event){

		$.ajax({
			data : {
			},

			type : 'GET',
			url : '/analyze',

			success: function(response){
				if (response)
				{
					var res = JSON.parse(response);

					console.log(res)

					if (res.response == "OK")
					{
						swal("Finished!","Analyzation has been finished!");
					}
				}
			}
		})

	});


	$('#view').on('click', function(event){

	$.ajax({
			data : {
			},

			type : 'GET',
			url : '/view',

			success: function(response){
				if (response)
				{
					var res = JSON.parse(response);

					chart(res.hashtags_list, res.count_list);
				}
			}
		})

		event.preventDefault();
	});
});