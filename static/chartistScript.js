var myChart;
var timeline = 'sec';

// empty graph created when app has just started
var data = {
    // A labels array that can contain any sort of values
    labels: [-10, -9, -8, -7, -6, -5, -4, -3, -2, -1],
    // Our series array that contains series objects or in this case series data arrays
    series: []
};

var options = {
    height: 500,
    axisY: {
	type: Chartist.FixedScaleAxis,
	high: 100,
	low: -100,
	ticks: [-100, -90, -80, -70, -60, -50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    },
    lineSmooth: Chartist.Interpolation.cardinal({
	fillHoles:true,
    })
};
myChart = new Chartist.Line('#chart1', data, options);
document.getElementById("last_update").innerHTML = "Graph last updated: ";

//update table
function updateTable(polarity, prevalence, influence) {
    //update polarity
    document.getElementById("pol-1").innerHTML = polarity[0]
    document.getElementById("pol-2").innerHTML = polarity[1]
    document.getElementById("pol-3").innerHTML = polarity[2]
    document.getElementById("pol-4").innerHTML = polarity[3]
    document.getElementById("pol-5").innerHTML = polarity[4]
    document.getElementById("pol-6").innerHTML = polarity[5]
    document.getElementById("pol-7").innerHTML = polarity[6]
    document.getElementById("pol-8").innerHTML = polarity[7]
    document.getElementById("pol-9").innerHTML = polarity[8]
    document.getElementById("pol-10").innerHTML = polarity[9]
    //update prevalence
    document.getElementById("pre-1").innerHTML = prevalence[0]
    document.getElementById("pre-2").innerHTML = prevalence[1]
    document.getElementById("pre-3").innerHTML = prevalence[2]
    document.getElementById("pre-4").innerHTML = prevalence[3]
    document.getElementById("pre-5").innerHTML = prevalence[4]
    document.getElementById("pre-6").innerHTML = prevalence[5]
    document.getElementById("pre-7").innerHTML = prevalence[6]
    document.getElementById("pre-8").innerHTML = prevalence[7]
    document.getElementById("pre-9").innerHTML = prevalence[8]
    document.getElementById("pre-10").innerHTML = prevalence[9]
    //update influence
    document.getElementById("inf-1").innerHTML = influence[0]
    document.getElementById("inf-2").innerHTML = influence[1]
    document.getElementById("inf-3").innerHTML = influence[2]
    document.getElementById("inf-4").innerHTML = influence[3]
    document.getElementById("inf-5").innerHTML = influence[4]
    document.getElementById("inf-6").innerHTML = influence[5]
    document.getElementById("inf-7").innerHTML = influence[6]
    document.getElementById("inf-8").innerHTML = influence[7]
    document.getElementById("inf-9").innerHTML = influence[8]
    document.getElementById("inf-10").innerHTML = influence[9]    
}


// update list
function updateList(arg1) {
    document.getElementById('tweet-list').innerHTML ="";	  
    var tweets = arg1;
    for (var t = 0; t < tweets.length; t++) {
	var text = tweets[t][0];
	var li_class = '\"neutraltweet\"';
	if (tweets[t][1] == 'pos') {
	    li_class = '\"postweet\"';
	} else if (tweets[t][1] == 'neg') {
	    li_class = '\"negtweet\"';
	}
	document.getElementById('tweet-list').innerHTML += ('<li class='+li_class+'>'+text+'</li>');
    }
}


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
	    labels: [-10, -9, -8, -7, -6, -5, -4, -3, -2, -1],
	    series: [{
		name: 'series-1',
		data: results.y1i
	    }, {
		name: 'series-2',
		data: results.y2i
	    }, {
		name: 'series-3',
		data: results.y3i
	    }]
	};	
	myChart.update(data);
	updateTable(results.tb1, results.tb2, results.tb3)
	updateList(results.tweets)
    });
    document.getElementById("last_update").innerHTML = "Graph last updated: " + Date();
}

//alert('Alerts are working!');
