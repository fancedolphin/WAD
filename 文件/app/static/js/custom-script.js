document.addEventListener('DOMContentLoaded', function() {
    fetchAllColleges();  // 调用获取所有学院信息的函数
    fetchAllCourses();  // 现有的调用获取所有课程信息的函数
    fetchAllMajors();
    document.getElementById('college').addEventListener('change', function() {
        var collegeId = this.value;
        updateCourses(collegeId);  // 当学院选择变更时更新课程信息
        updateMajors(collegeId);
    });
});

function fetchAllColleges() {
    fetch('/getCollege')
    .then(response => response.json())
    .then(data => {
        populateColleges(data);
    })
    .catch(error => console.error('Error fetching colleges:', error));
}

function populateColleges(colleges) {
    var collegeSelect = document.getElementById('college');
    collegeSelect.innerHTML = '';  // 清空现有选项

    // 为每个学院创建一个新的<option>元素并添加到下拉列表中
    colleges.forEach(college => {
        var option = new Option(college.college_name, college.college_no);
        collegeSelect.appendChild(option);
    });
}
    function fetchAllCourses() {
        fetch('/getAllCourses')
        .then(response => response.json())
        .then(data => {
            populateCourses(data);
        })
        .catch(error => console.error('Error fetching courses:', error));
    }

    function populateCourses(courses) {
        var coursesSelect = document.getElementById('courses_no');
        coursesSelect.innerHTML = ''; // 清空现有选项

        // 为每个课程创建一个新的<option>元素并添加到下拉列表中
        courses.forEach(course => {
            var option = new Option(course.course_name, course.course_no);
            coursesSelect.appendChild(option);
        });
    }

    function updateCourses(collegeId) {
        // 根据特定的学院ID筛选课程，这需要后端API支持按学院ID筛选，或者在前端进行过滤
        fetch(`/getCoursesByCollege/${collegeId}`)
        .then(response => response.json())
        .then(data => {
            populateCourses(data);  // 使用新的课程数据填充课程下拉列表
        })
        .catch(error => console.error('Error fetching courses by college:', error));
    }
function fetchAllMajors() {
    // 假设一个类似的后端路由提供所有专业
    fetch('/getMajor')
    .then(response => response.json())
    .then(data => {
        populateMajors(data);
    })
    .catch(error => console.error('Error fetching majors:', error));
}

function populateMajors(majors) {
    var majorSelect = document.getElementById('major');
    majorSelect.innerHTML = ''; // 清空现有选项

    // 为每个专业创建一个新的<option>元素并添加到下拉列表中
    majors.forEach(major => {
        var option = new Option(major.major_name,major.major_no);
        majorSelect.appendChild(option);
    });
}

function updateMajors(collegeId) {
    // 根据学院ID请求专业数据，假设后端能够根据学院ID筛选专业
    fetch(`/getMajorsByCollege/${collegeId}`)
    .then(response => response.json())
    .then(data => {
        populateMajors(data);
    })
    .catch(error => console.error('Error fetching majors by college:', error));
}