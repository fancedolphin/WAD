var get_table_url = ''
var csrf_token = $('#csrf_token').val()
var init_major_arr = []
var init_courses_arr = []

// 获取学院
function getCollege() {
    var college = []
    $.ajax({
        type: "GET",
        url: "/getCollege",
        data: '',
        dataType: "json",
        async: false,
        success: function (data) {
            // console.log(data);
            college = data
        }
    });
    return college
}

// 获取专业
function getMajor() {
    var major = []
    $.ajax({
        type: "GET",
        url: "/getMajor",
        data: '',
        dataType: "json",
        async: false,
        success: function (data) {
            // console.log(data);
            major = data
        }
    });
    return major
}

// 初始化学院选项
function initCollege(current_college_no) {
    $('#college').find("option:not(:first)").remove();
    $.each(college, function (i, item) {
        if (current_college_no == item.college_no) {
            $('#college').append(`<option value="${item.college_no}" selected>${item.college_name}</option>`)
        } else {
            $('#college').append(`<option value="${item.college_no}">${item.college_name}</option>`)
        }
    })
}

// 初始化专业选项
function initMajor(college_, current_major_no) {
    init_major_arr = []
    var c_no = college_ ? college_ : $('#college').val()

    if (c_no != undefined && c_no != null) {
        $.each(major, function (i, m) {
            if (m.college_no === c_no) {
                init_major_arr.push(m)
            }
        })
    }

    $.each(init_major_arr, function (i, item) {
        if (current_major_no == item.major_no) {
            $('#major').append(`<option value="${item.major_no}" selected>${item.major_name}</option>`)
        } else {
            $('#major').append(`<option value="${item.major_no}">${item.major_name}</option>`)
        }

    })

    $('#major').selectpicker('refresh');
}

// 获取所有课程
function getAllCourses() {
    $.ajax({
        type: "GET",
        url: "/getAllCourses",
        data: '',
        dataType: "json",
        async: false,
        success: function (data) {
            console.log(data);
            courses = data
        }
    });
    return courses
}

// 初始化课程选项
function initCourses(college_) {
    init_courses_arr = []
    var c_no = college_ ? college_ : $('#college').val()
    if (c_no != undefined && c_no != null) {
        $.each(courses, function (i, m) {
            if (m.college_no === c_no) {
                init_courses_arr.push(m)
            }
        })
    }

    $.each(init_courses_arr, function (i, item) {
        $('#courses_no').append('<option value="' + item.course_no + '">' + item.course_name +
            '</option>')
    })

    $('#courses_no').selectpicker('refresh');
}