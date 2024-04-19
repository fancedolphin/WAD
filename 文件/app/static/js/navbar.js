student_navbar = `
    <li class="nav-item active">
        <a class="nav-link" href="/home">Home</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="/personal_information">Personal</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="/score_query">Grade</a>
    </li>
        <li class="nav-item">
        <a class="nav-link" href="/isChoosed_course">Chose Course</a>
    </li>
       </li>
        <li class="nav-item">
        <a class="nav-link" href="/choose_course">Choose Course</a>
    </li>
     
    `
teacher_navbar = `
    <li class="nav-item active">
        <a class="nav-link" href="/home">Home</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="/personal_information">Personal</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="/add_score">Enter Grade</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="/course_setup">Course Settting</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="/add_teacher_course">Add course</a>
    </li>
`
manager_navbar = `
    <li class="nav-item active">
        <a class="nav-link" href="/home">Home</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="/managing_users">User manage</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="/edit_password">Modify password</a>
    </li>
        <li class="nav-item">
        <a class="nav-link" href="/managing_college">College</a>
    </li>
        <li class="nav-item">
        <a class="nav-link" href="/managing_major">Major</a>
    </li>
        <li class="nav-item">
        <a class="nav-link" href="/managing_course">Course</a>
    </li>

`

// 获取路由参数
function getUrlOption() {
    let href = window.location.href
    let query = href.substring(href.indexOf('?') + 1);
    let vars = query.split("&");
    let obj = {}
    for (var i = 0; i < vars.length; i++) {
        let pair = vars[i].split("=");
        obj[pair[0]] = pair[1]
    }
    return obj;
}

user_role = getUrlOption().user_role
user_role ? localStorage.setItem('role', user_role) : ''
user_role = localStorage.getItem('role')

// 导航
if (user_role == '1') {
    $('.navbar-nav.mr-auto').empty()
    $('.navbar-nav.mr-auto').append(student_navbar)
} else if (user_role == '2') {
    $('.navbar-nav.mr-auto').empty()
    $('.navbar-nav.mr-auto').append(teacher_navbar)
} else if (user_role == '0') {
    $('.navbar-nav.mr-auto').empty()
    $('.navbar-nav.mr-auto').append(manager_navbar)
} 
