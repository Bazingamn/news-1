$(document).ready(function() {
    layui.use(['layer'], function() {
        getCard2Data = function() {
            $.ajax({
                url: '/web/getTodayData/',
                method: 'POST',
                success: function(res) {
                    if (res.code == 0) {
                        console.log($(".data-item-num").length)
                        console.log($(".data-item-num").eq(0).val())
                        $(".data-item-num").eq(0).text(res.data.news_num)
                        $(".data-item-num").eq(1).text(res.data.video_num)
                        $(".data-item-num").eq(2).text(res.data.user_num)
                    } else {
                        parent.layer.msg(res.data, { time: 500 })
                    }
                },
                fail: function(res) {
                    parent.layer.msg('连接服务器失败', { time: 500 })
                }
            })
            $.ajax({
                url: '/web/getAllData/',
                method: 'POST',
                success: function(res) {
                    if (res.code == 0) {
                        $(".data-item-num").eq(3).text(res.data.news_num)
                        $(".data-item-num").eq(4).text(res.data.video_num)
                        $(".data-item-num").eq(5).text(res.data.registed_user_num)
                        $(".data-item-num").eq(6).text(res.data.user_num)
                    } else {
                        parent.layer.msg(res.data, { time: 500 })
                    }
                },
                fail: function(res) {
                    parent.layer.msg('连接服务器失败', { time: 500 })
                }
            })
        }
        getCard2Data()
        setInterval(function() {
            getCard2Data()
        }, 1000 * 60)
    })
})