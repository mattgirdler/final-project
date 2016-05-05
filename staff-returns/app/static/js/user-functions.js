function selectUser() {
    var xhttp = new XMLHttpRequest();
    var user_id = document.getElementById('user').value;
    if (user_id != 'Select a user') {
        xhttp.onreadystatechange = function () {
            if (xhttp.readyState == 4 && xhttp.status == 200) {
                var user = JSON.parse(xhttp.responseText);
                console.log(user);

            }
        };
        xhttp.open("GET", "http://192.168.33.10:8080/load-user/"+user_id, true);
        xhttp.send();
    }
}

$(document).ready(function() {
    setTimeout(function() {
        selectUser()
    }, 1000);
});