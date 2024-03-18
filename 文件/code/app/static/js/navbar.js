student_navbar = `
    <li class="nav-item active">
        <a class="nav-link" href="/home">首页</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="/personal_information">个人中心</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="/score_query">成绩查询</a>
    </li>
    <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" href="#" role="button" data-toggle="dropdown" aria-expanded="false">
            选课
        </a>
        <div class="dropdown-menu">
            <a class="dropdown-item" href="/isChoosed_course">已选</a>
            <a class="dropdown-item" href="/choose_course">选课</a>
        </div>
    </li>
    `
teacher_navbar = `
    <li class="nav-item active">
        <a class="nav-link" href="/home">首页</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="/personal_information">个人中心</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="/add_score">录入成绩</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="/course_setup">课程设置</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="/add_teacher_course">添加课程</a>
    </li>
`
manager_navbar = `
    <li class="nav-item active">
        <a class="nav-link" href="/home">首页</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="/managing_users">用户管理</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="/edit_password">修改密码</a>
    </li>
    <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" href="#" role="button" data-toggle="dropdown" aria-expanded="false">
            更多
        </a>
        <div class="dropdown-menu">
            <a class="dropdown-item" href="/managing_college">学院管理</a>
            <a class="dropdown-item" href="/managing_major">专业管理</a>
            <a class="dropdown-item" href="/managing_course">课程管理</a>
        </div>
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
