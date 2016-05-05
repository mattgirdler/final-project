function selectUser() {
    var xhttp = new XMLHttpRequest();
    var user_id = document.getElementById('username').value;
    if (user_id != 'Select a user') {
        xhttp.onreadystatechange = function () {
            if (xhttp.readyState == 4 && xhttp.status == 200) {
                var user = JSON.parse(xhttp.responseText);
                showUserDiv();
                fillForm(user);
            }
        };
        xhttp.open("GET", "http://192.168.33.10:8080/load-user/"+user_id, true);
        xhttp.send();
    } else {
        hideUserDiv();
    }
}

function fillForm(user) {
    document.getElementById('firstname').value = user['firstname'];
    document.getElementById('lastname').value = user['lastname'];
    document.getElementById('role').value = user['role'];
    document.getElementById('paygrade').value = user['paygrade'];
}

function hideUserDiv() {
    document.getElementById('hidden_div').style.visibility = "hidden";
}

function showUserDiv() {
    document.getElementById('hidden_div').style.visibility = "visible";
}

$(document).ready(function() {
    setTimeout(function() {
        selectUser()
    }, 1000);
});