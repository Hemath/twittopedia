function chart(cat, dat)
{
	
	var chart = {
		type:'column'
	};

	var title = {
		text:'Top 10 Hashtags'
	};

	var subtitle = {
		text: "A small Analytics"
	};

	var xAxis = {
		categories:cat,
		crosshair : true
	};

	var yAxis = {
		min : 0,
		title:
		{
			text:"Count"
		}
	};

	var series = [
	{
		name:"Hashtags",
		data : dat
	}];

	var json = {};
	json.chart = chart;
	json.title = title;
	json.subtitle = subtitle;
	json.xAxis = xAxis;
	json.yAxis = yAxis;
	json.series = series;
	$("#chart").highcharts(json);
}

//chart(["#1","#2","#3","#4","#5","#6","#7","#8","#9","#10"],[1,2,3,4,5,6,7,8,9,10]);