var courseData1 = Array.from({ length: 8 }, () => Array.from({ length: 7 }, () => ""));
fetch('/api/course-table')
    .then(response => response.json())
    .then(data => {
        for (var i =0;i<data.length;i++){
            var sectionIndex = parseInt(data[i].section)-1;
            var day = parseInt(data[i].day) - 1;
            courseData1[sectionIndex][day] = data[i]
        }
        console.log(courseData1);
    })
    .catch(error => console.error('Error fetching course table:', error));


function populateTable() {
    var table = document.getElementById("course list");
    var tbody = table.getElementsByTagName("tbody")[0];

    for (var i = 0; i < courseData1.length; i++) {
        var row = tbody.insertRow();
        if (i === 3) {
            var breakRow = tbody.insertRow();
            var breakCell = breakRow.insertCell();
            breakCell.textContent = "Noon break";
            breakCell.colSpan = 8;
            breakCell.style.textAlign = "center";
            breakCell.style.fontSize = "30px";
            var lightPink = "rgba(255, 182, 193, 0.5)";
            breakCell.style.backgroundColor = lightPink;
            breakCell.style.fontWeight = "bold";
        }
        var numberCell = row.insertCell();
        numberCell.textContent = i + 1;
        numberCell.style.backgroundColor = 'blue';
        numberCell.style.color = "white"
        numberCell.style.fontWeight = "bold";

        for (var j = 0; j < courseData1[i].length; j++) {
            var cell = row.insertCell();
            var courseName = courseData1[i][j].course_name;
            var className = courseData1[i][j].class;
            var instructor = courseData1[i][j].instructor;
            var span = document.createElement("span");
            span.textContent = courseName;
            span.style.fontWeight = 550;
            span.title = "Course information：" + getCourseInfo(className,instructor);
            span.className = "course";
            cell.appendChild(span);
        }
    }
}

function getCourseInfo(className,instructor) {
    return "class: " + className + '\n' + "Instructor: " + instructor;
}

window.onload = populateTable;
