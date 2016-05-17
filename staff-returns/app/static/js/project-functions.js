google.charts.load('current', {packages: ['corechart']});

function prepareProjectData(project, year, month){
    var data_array = [['User', 'Hours', 'Cost (£)']];
    if (project[year] && project[year][month] && project[year][month]['users']){
        for (var user in project[year][month]['users']) {
            data_array.push([user, parseFloat(project[year][month]['users'][user]['hours']), parseFloat(project[year][month]['users'][user]['cost'])]);
        }
    }
    return data_array
}

function prepareUserData(user, year, month) {
    var data_array = [['Project', 'Hours']];
    if (user[year] && user[year][month] && user[year][month]['projects']){
        for (var project in user[year][month]['projects']) {
            console.log(user[year][month]['projects'][project])
            data_array.push([project, parseFloat(user[year][month]['projects'][project])]);
        }
    }
    return data_array
}

function drawPieChart(subject, year, month, type) {
    // Define the chart to be drawn.
    if (type == 'project') {
        var data_array = prepareProjectData(subject, year, month)
        var div = 'project_chart_div'
    } else if (type == 'user') {
        var data_array = prepareUserData(subject, year, month)
        var div = 'user_chart_div'
    }
    var data = new google.visualization.arrayToDataTable(data_array);
    // Instantiate and draw the chart.
    var chart = new google.visualization.PieChart(document.getElementById(div));
    var options = {
        title: 'Hours logged',
        height: "100%",
        width: "100%",
    };
  chart.draw(data, options);
}

function drawColumnChart(project, year, month, type) {
    if (type == 'project') {
        var data_array = prepareProjectData(project, year, month);
        var total_hours = project[year][month]['total_hours']
        var total_cost = project[year][month]['total_cost']
        var div = 'project_chart_div'
        document.getElementById('total_hours_div').innerHTML = "Monthly hours logged: " + total_hours
        document.getElementById('total_cost_div').innerHTML = "Monthly cost: £" + total_cost
    } else if (type == 'user') {
        var data_array = prepareUserData(project, year, month);
        //var hours_logged = user[year][month]['total_hours'];
        //var hours_required = user[year][month]['hours_required'];
        var div = 'user_chart_div'
        //document.getElementById('user_hours_logged_div').innerHTML = "Total monthly hours logged: " + hours_logged
        //document.getElementById('user_hours_required_div').innerHTML = "Total monthly hours required: " + hours_required

    }
    var data = google.visualization.arrayToDataTable(data_array);
    var chart = new google.visualization.ColumnChart(document.getElementById(div));
    var options = {
        title: 'Hours/cost logged',
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
    document.getElementById('total_hours_div').innerHTML = "Monthly hours logged: 0"
    document.getElementById('total_cost_div').innerHTML = "Monthly cost: £0"
    var data = new google.visualization.arrayToDataTable(data_array);
    // Instantiate and draw the chart.
    var chart = new google.visualization.PieChart(document.getElementById('project_chart_div'));
    var options = {
        title: 'Hours logged',
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
    document.getElementById('total_hours_div').innerHTML = "Monthly hours logged: 0"
    document.getElementById('total_cost_div').innerHTML = "Monthly cost: £0"
    var data = new google.visualization.arrayToDataTable(data_array);
    // Instantiate and draw the chart.
    var chart = new google.visualization.ColumnChart(document.getElementById('project_chart_div'));
    var options = {
        title: 'Hours logged',
        height: "100%",
        width: "100%",
    };
    chart.draw(data, options);
}

function drawProjectChart(project) {
    var chartType =  document.getElementById("project_chart").value;
    var month = document.getElementById("project_month").value;
    var year = document.getElementById("project_year").value;
    if (project[year] && project[year][month] && (!jQuery.isEmptyObject(project[year][month]['users']))) {
        switch (chartType) {
            case 'Column' :
                drawColumnChart(project, year, month, 'project');
                break;
            case 'Pie' :
                drawPieChart(project, year, month, 'project');
                break;
        }
    } else {
        switch (chartType) {
            case 'Column' :
                drawEmptyColumnChart();
                break;
            case 'Pie' :
                drawEmptyPieChart();
                break;
        }
    }
}

function drawUserChart(user) {
    var chartType =  document.getElementById("user_chart").value;
    var month = document.getElementById("user_month").value;
    var year = document.getElementById("user_year").value;
    if (user[year] && user[year][month] && (!jQuery.isEmptyObject(user[year][month]['projects']))) {
        switch (chartType) {
            case 'Column' :
                drawColumnChart(user, year, month, 'user');
                break;
            case 'Pie' :
                drawPieChart(user, year, month, 'user');
                break;
        }
    } else {
        switch (chartType) {
            case 'Column' :
                drawEmptyColumnChart();
                break;
            case 'Pie' :
                drawEmptyPieChart();
                break;
        }
    }
}


function loadProject() {
    var xhttp = new XMLHttpRequest();
    var projectName = document.getElementById("project").value;
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            var project = JSON.parse(xhttp.responseText);
            drawProjectChart(project);
            generateProjectReport(project)
        }
    };
    xhttp.open("GET", "http://192.168.33.10:8080/load-project/"+projectName, true);
    xhttp.send();
}

function loadUser() {
    var xhttp = new XMLHttpRequest();
    var userName = document.getElementById("user").value;
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            var user = JSON.parse(xhttp.responseText);
            drawUserChart(user);
            generateUserReport(user)
        }
    };
    xhttp.open("GET", "http://192.168.33.10:8080/load-user/"+userName, true);
    xhttp.send();
}


function generateProjectReport(project) {
    var month = document.getElementById("project_month").value;
    var year = document.getElementById("project_year").value;
    if (project[year] && project[year][month] && project[year][month]['users']) {
        var data = "text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(project[year][month]));
        var button = document.getElementById('project_report')
        button.href = 'data:' + data;
        button.download = project['_id'] + month + year + '.json';
    } else {

    }
}

function generateUserReport(user) {
    var month = document.getElementById("user_month").value;
    var year = document.getElementById("user_year").value;
    if (user[year] && user[year][month] && user[year][month]['projects']) {
        var data = "text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(user[year][month]));
        var button = document.getElementById('user_report')
        button.href = 'data:' + data;
        button.download = user['_id'] + month + year + '.json';
    } else {

    }
}

$('#tabs a[href="#project_tab"]').click(function (e) {
    console.log('Worked')
    loadProject()
})

$('#tabs a[href="#user_tab"]').click(function (e) {
    console.log('Worked')
    loadUser()
})

//create trigger to resizeEnd event
$(window).resize(function() {
    if(this.resizeTO) clearTimeout(this.resizeTO);
    this.resizeTO = setTimeout(function() {
        $(this).trigger('resizeEnd');
    }, 500);
});

//redraw graph when window resize is completed
$(window).on('resizeEnd', function() {
    loadProject();
    loadUser();
});


$(document).ready(function() {
    setTimeout(function() {
        loadProject();
        loadUser();
    }, 2000);
});