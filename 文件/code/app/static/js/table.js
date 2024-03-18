$(function () {
    initTable()
})

var total = 0//总数
var pageNum = 1//页码
var pageSize = 5//每页数量
var isPage = false//是否点击分页
var isSearch = false
var isChoose = false

// 初始化表单
function initTable(url) {
    var table = []

    $.ajax({
        type: "get",
        url: url ? url : get_table_url + "/getTable",
        data: '',
        dataType: "json",
        async: false,
        success: function (data) {
            console.log(data);
            table = data
            total = table.length
        }
    });
    render(table)

    return table
}

// 渲染
function render(table) {
    console.log(table);

    if (table.length === 0) {
        $('tbody').empty()
        $('tbody').append(`
        <tr class='none'>
            <td colspan=7>暂无数据
            <td>
        </tr>
        `)
        return false
    }
    chooseBtn()

    if (pageNum != 1 && isPage) {
        $('tbody').empty()
        handleFormat(table)
        return false
    } else if (pageNum === 1 && isPage) {
        $('tbody').empty()
        handleFormat(table)
    } else {
        console.log('--------');
        pageNavigation()
        if (isSearch || isChoose) {
            $('tbody').empty()
            handleFormat(table)
        }

    }

}

// 选课按钮
function chooseBtn() {
    $('.choose-class-btn').each((i, item) => {
        if (item.attributes[2].value == 0 && get_table_url == '/choose_score') {
            item.classList.value = 'btn choose-class-btn btn-secondary'
        }
    })
}

// 请求表单数据
function handleFormat(table) {
    $.each(table, function (i, item) {
        if (item.grade == '' || item.grade == null) {
            item.grade = '暂无'
        }

        if (i >= 5) return false

        num = (pageNum - 1) * pageSize + i + 1

        switch (get_table_url) {
            case "/choose_course":
                $('tbody').append(` <tr class="item">
                <th scope="row">${num}</th>
                <td>${item.course_name}</td>
                <td>${item.course_no}</td>
                <td>${item.credit}</td>
                <td>${item.course_hour}</td>
                <td>${item.teacher_name}</td>
                <td>
                    <button type="button" class="btn ${item.course_capacity != 0 ? 'btn-success' : 'btn-secondary'} choose-class-btn" data-course-capacity="${item.course_capacity}"
                      data-classid="${item.course_no}" onclick="handleChoosed(${item.course_capacity}, ${item.course_no})">选课</button>
                </td>
            </tr>`)
                break;
            case "/isChoosed_course":
                $('tbody').append(` <tr class="item">
                <th scope="row">${num}</th>
                <td>${item.course_name}</td>
                <td>${item.course_no}</td>
                <td>${item.credit}</td>
                <td>${item.course_hour}</td>
                <td>${item.teacher_name}</td>
                <td>
                    <button type="button" class="btn btn-success choose-class-btn" data-course-capacity="${item.course_capacity}"
                      data-classid="${item.course_no}" onclick="handleChoosed(${item.course_capacity}, ${item.course_no})">取消选课</button>
                </td>
            </tr>`)
                break;
            case "/score_query":
                $('tbody').append(` <tr class="item">
                <th scope="row">${num}</th>
                <td>${item.course_name}</td>
                <td>${item.course_no}</td>
                <td>${item.credit}</td>
                <td>${item.course_hour}</td>
                <td>${item.teacher_name}</td>
                <td>${item.grade}</td>
            </tr>`)
                break;
            default:
                break;
        }

    })
}

// 渲染分页按钮
function pageNavigation() {
    if (0 < total && total < 5) {
        $('.page-navigation').hide()
    } else {
        $('.page-navigation').show()
        pageSize = 5
        $('.page-navigation').pagination({
            pages: Math.ceil(total / pageSize), //总页数
            edges: 2,
            cssStyle: '', //按纽大小pagination-lg或写入自定义css
            displayedPages: 3, //显示几个
            onPageClick: function (pageNumber, event) {
                //点击时调用
                isPage = true
                pageNum = pageNumber
                var url = 'http://127.0.0.1:1208' + get_table_url + '?page=' + pageNumber + '&is_page=1'
                initTable(url)
            },
            onInit: function (getid) {
                //刷新时或初始化调用

            }

        });
    }
}

// 模糊搜索
$('.search-input').change(function (e) {
    var search = e.target.value
    if (search.trim() == '') {
        isSearch = true
        url = 'http://127.0.0.1:1208' + get_table_url + '/getTable'
        initTable(url)

        $("tbody tr").show()
    } else {
        $("tbody tr").hide()
        $("tbody tr td").filter(":contains(" + search.trim() + ")").parents('tr').show()
    }
})

// 点击搜索
$('.search-btn').click(function () {
    var list = []
    var course_no = $('.search-input').val()
    if (course_no == '') {
        initTable()
        return false
    }
    $.ajax({
        type: "get",
        url: get_table_url + "/getSearch/" + course_no,
        data: '',
        dataType: "json",
        async: false,
        success: function (data) {
            console.log(data);
            if (data.code == 400) {
                $('.modal').show().find('.modal-title').text('信息')
                $('.modal').find('.modal-body p').text(data.msg)
                setTimeout(() => {
                    $('.modal').hide()
                }, 3000);
                return false
            }

            list = data
            isSearch = true
            render(list)
        }
    });
    return false

})

// 弹框
$('.modal-close-btn').click(function () {
    $('.modal').hide()
})
$('.modal-confirm-btn').click(function () {
    if (get_table_url == '/isChoosed_course') {
        cancelChoose(cancel_course_no)
    }
    $('.modal').hide()
})


