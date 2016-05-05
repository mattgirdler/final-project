function addProjectRow() {
    for (var i = 1; i < 16; i++) {
        var div = document.getElementById('project_row_' + i)
        if (isHidden(div)) {
            div.style.display = ""
            break;
        }
    }
}

function isHidden(el) {
    var style = window.getComputedStyle(el);
    return (style.display === 'none')
}

function clicked() {
    return confirm('Are you sure you want to save? This will overwrite any previously saved projects for this month.');
}