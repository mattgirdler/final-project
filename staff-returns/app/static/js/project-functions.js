google.charts.load('current', {packages: ['corechart', 'table']});

function prepareData(project, year, month){
    var data_array = [['User', 'Hours', 'Cost (£)']];
    console.log(project)
    if (project[year] && project[year][month] && project[year][month]['users']){
        for (var user in project[year][month]['users']) {
            data_array.push([user, parseInt(project[year][month]['users'][user]['hours']), parseInt(project[year][month]['users'][user]['cost'])]);
        }

    }
    return data_array
}

// function getTotalHours(project):

function drawPieChart(project, year, month) {
    // Define the chart to be drawn.
    var data_array = prepareData(project, year, month)
    var total_hours = project[year][month]['total_hours']
    var data = new google.visualization.arrayToDataTable(data_array);
    // Instantiate and draw the chart.
    var chart = new google.visualization.PieChart(document.getElementById('project_chart'));
    var options = {
        title: 'Hours logged',
        //chartArea:{left:80,top:50,width:"80%",height:"100%"},
        height: "100%",
        width: "100%",
        //backgroundColor: "#F4F4F4"
    };
  chart.draw(data, options);
}

function drawColumnChart(project, year, month) {
    var data_array = prepareData(project, year, month);
    var total_hours = project[year][month]['total_hours']
    var total_cost = project[year][month]['total_cost']
    document.getElementById('total_hours_div').innerHTML = "Total monthly hours logged: " + total_hours
    document.getElementById('total_cost_div').innerHTML = "Total monthly cost: £" + total_cost
    var data = google.visualization.arrayToDataTable(data_array);
    var chart = new google.visualization.ColumnChart(document.getElementById('project_chart'));
    var options = {
        title: 'Hours/cost logged',
        //chartArea:{left:80,top:0,width:"80%",height:"100%"},
        height: "100%",
        width: "100%",
    };
    chart.draw(data, options);
}

function drawTable(project, year, month) {
    var data_array = prepareData(project, year, month)
    var data = new google.visualization.arrayToDataTable(data_array);
    var chart = new google.visualization.Table(document.getElementById('project_chart'));
    var options = {
        title: 'Hours/cost logged',
        //chartArea:{left:80,top:50,width:"80%",height:"100%"},
        height: "100%",
        width: "100%",
    };
    chart.draw(data, options);
}

function drawEmptyPieChart() {
    // Define the chart to be drawn.
    data_array = [
        ['Hours', 'Hours', 'Cost (£)'],
        ['', 0, 0],
    ]
    document.getElementById('total_hours_div').innerHTML = "Total monthly hours logged: 0"
    document.getElementById('total_cost_div').innerHTML = "Total monthly cost: £0"
    var data = new google.visualization.arrayToDataTable(data_array);
    // Instantiate and draw the chart.
    var chart = new google.visualization.PieChart(document.getElementById('project_chart'));
    var options = {
        title: 'Hours logged',
        //chartArea:{left:80,top:50,width:"80%",height:"100%"},
        height: "100%",
        width: "100%",
    };
    chart.draw(data, options);
}

function drawEmptyColumnChart() {
    // Define the chart to be drawn.
    data_array = [
        ['Hours', 'Hours', 'Cost (£)'],
        ['', 0, 0],
    ]
    document.getElementById('total_hours_div').innerHTML = "Total monthly hours logged: 0"
    document.getElementById('total_cost_div').innerHTML = "Total monthly cost: £0"
    var data = new google.visualization.arrayToDataTable(data_array);
    // Instantiate and draw the chart.
    var chart = new google.visualization.ColumnChart(document.getElementById('project_chart'));
    var options = {
        title: 'Hours logged',
        //chartArea:{left:80,top:50,width:"80%",height:"100%"},
        height: "100%",
        width: "100%",
    };
    chart.draw(data, options);
}


function loadProject() {
    var xhttp = new XMLHttpRequest();
    var projectName = document.getElementById("project").value;
    var chartType =  document.getElementById("chart").value;
    var month = document.getElementById("month").value;
    var year = document.getElementById("year").value;
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            var project = JSON.parse(xhttp.responseText);
            if (project[year] && project[year][month] && project[year][month]['users']) {
                switch (chartType) {
                    case 'Column' :
                        drawColumnChart(project, year, month);
                        document.getElementById('hidden_div').style.visibility = "hidden"
                        break;
                    case 'Pie' :
                        drawPieChart(project, year, month);
                        document.getElementById('hidden_div').style.visibility = "hidden"
                        break;
                    case 'Table':
                        drawTable(project, year, month);
                        document.getElementById('hidden_div').style.visibility = "hidden"
                        break;
                }
            } else {
                switch (chartType) {
                    case 'Column' :
                        drawEmptyColumnChart(project);
                        document.getElementById('hidden_div').style.visibility = "visible"
                        break;
                    case 'Pie' :
                        drawEmptyPieChart();
                        document.getElementById('hidden_div').style.visibility = "visible"
                        break;
                    case 'Table':
                        drawTable(project)
                        break;
                }
            }
        }
    };
    xhttp.open("GET", "http://192.168.33.10:8080/load-project/"+projectName, true);
    xhttp.send();
}

function printChart() {
    var chart_div = document.getElementById("project_chart");
    var chart_value =  document.getElementById("chart").value;
    switch(chart_value) {
        case 'Column':
            var chart = new google.visualization.ColumnChart(chart_div);
            break;
        case 'Pie':
            var chart = new google.visualization.PieChart(chart_div);
            break;
    }
    console.log(chart);
    google.visualization.events.addListener(chart, 'ready', function () {
      chart.innerHTML = '<img src="' + chart.getImageURI() + '">';
    });
    window.print(chart)
}


$(document).ready(function() {
    setTimeout(function() {
        loadProject()
    }, 2000);
});