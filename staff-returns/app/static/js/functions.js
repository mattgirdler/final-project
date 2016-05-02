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

var div = document.getElementById('workingpattern-1')