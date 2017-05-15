var myChart;
var timeline = 'sec';

// empty graph created when app has just started
var data = {
    // A labels array that can contain any sort of values
    labels: [],
    // Our series array that contains series objects or in this case series data arrays
    series: []
};

var options = {
    height: 500,
    axisY: {
	type: Chartist.FixedScaleAxis,
	high: 100,
	low: 0,
	ticks: [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    }
};
myChart = new Chartist.Line('#chart1', data, options);
document.getElementById("last_update").innerHTML = "Graph last updated: ";

// update chart
function updateChart(arg1, arg2) {
    //    alert('updating chart!');
    var query_id = arg1;
    if (typeof arg2 === 'string') {
	timeline = arg2;
    }
    var updatedData = $.get('search/' + query_id.toString() + '/data/' + timeline);
    updatedData.done(function(results) {

	var data = {
	    labels: results.xs,
	    series: [
		results.yi
	    ]
	};	
	myChart.update(data);
    });
    document.getElementById("last_update").innerHTML = "Graph last updated: " + Date();
}

//alert('Alerts are working!');
