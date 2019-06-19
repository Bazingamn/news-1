$(document).ready(function() {
    layui.use(['layer', 'laydate'], function() {
        function getNewDay(dateTemp, days) {
            var dateTemp = dateTemp.split("-");
            var nDate = new Date(dateTemp[1] + '-' + dateTemp[2] + '-' + dateTemp[0]); //转换为MM-DD-YYYY格式    
            var millSeconds = Math.abs(nDate) + (days * 24 * 60 * 60 * 1000);
            var rDate = new Date(millSeconds);
            var year = rDate.getFullYear();
            var month = rDate.getMonth() + 1;
            if (month < 10) month = "0" + month;
            var date = rDate.getDate();
            if (date < 10) date = "0" + date;
            return (year + "-" + month + "-" + date);
        }
        var date = new Date();
        var today = date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate();
        console.log(today)
        $("#date1").val(getNewDay(today, -7))
        $("#date2").val(getNewDay(today, -1))
        var useChart = echarts.init(document.getElementById('use'));
        var registChart = echarts.init(document.getElementById('regist'));
        var use_data = null;
        var regist_data = null;
        var option = {
            title: {
                show: true,
                text: '',
                x: 'center',
                textStyle: {
                    fontSize: 18,
                    fontWeight: 'bolder',
                    color: '#333' // 主标题文字颜色
                },
            },
            xAxis: {
                type: 'category',
                color: 'blue',
                boundaryGap: false,
                data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                axisLabel: { //坐标轴刻度标签的相关设置。
                    interval: 0,
                    rotate: "-45",
                    fontSize: 10
                }
            },
            yAxis: {
                type: 'value',
                max: 10
            },
            series: [{
                data: [820, 932, 901, 934, 1290, 1330, 1320],
                smooth: true,
                type: 'line',
                areaStyle: {
                    color: '#6FBAE1'
                },
                itemStyle: {
                    normal: {
                        lineStyle: {
                            color: '#7AC7C0'
                        },
                        label: { show: true },
                        color: "#7AC7C0"
                    }
                }
            }]
        };
        $('#use_graph_title').mouseover(function() {
            option.xAxis.data = use_data.date
            option.yAxis.max = use_data.max
            option.series[0].data = use_data.data
            useChart.clear()
            useChart.setOption(option);
            $('#use_graph_title').addClass('graph-title-item-selected')
            $('#use_graph_title').removeClass("graph-title-item");
            $('#regist_graph_title').addClass('graph-title-item');
            $('#regist_graph_title').removeClass('graph-title-item-selected');
            $("#use_graph").show();
            $("#regist_graph").hide();
        });
        $('#regist_graph_title').mouseover(function() {
            option.xAxis.data = regist_data.date
            option.yAxis.max = regist_data.max
            option.series[0].data = regist_data.data
            registChart.clear()
            registChart.setOption(option);
            $('#regist_graph_title').addClass('graph-title-item-selected')
            $('#regist_graph_title').removeClass("graph-title-item");
            $('#use_graph_title').addClass('graph-title-item');
            $('#use_graph_title').removeClass('graph-title-item-selected');
            $("#regist_graph").show();
            $("#use_graph").hide();
        });
        getCard1Data = function() {
            var loading = parent.layer.load(0, {
                shade: false,
            });
            $.ajax({
                url: '/web/getUseRec/',
                method: 'POST',
                data: {
                    start_date: $("#date1").val(),
                    end_date: $("#date2").val(),
                },
                success: function(res) {
                    parent.layer.close(loading);
                    if (res.code == 0) {
                        option.xAxis.data = res.data.date
                        option.yAxis.max = res.data.max
                        option.series[0].data = res.data.data
                        use_data = res.data
                        useChart.setOption(option);
                    } else {
                        parent.layer.msg(res.data, { time: 500 })
                    }
                },
                fail: function(res) {
                    parent.layer.msg('连接服务器失败', { time: 500 })
                },
                complete: function() {
                    parent.layer.close(loading);
                }
            })
            $.ajax({
                url: '/web/getRegistRec/',
                method: 'POST',
                success: function(res) {
                    parent.layer.close(loading);
                    if (res.code == 0) {
                        option.xAxis.data = res.data.date
                        option.yAxis.max = res.data.max
                        option.series[0].data = res.data.data
                        regist_data = res.data
                        registChart.setOption(option);
                    } else {
                        parent.layer.msg(res.data, { time: 500 })
                    }
                },
                fail: function(res) {
                    parent.layer.msg('连接服务器失败', { time: 500 })
                },
                complete: function() {
                    parent.layer.close(loading);
                }
            })
        }
        getCard1Data()
        // setInterval(function() {
        //     getCard1Data()
        // }, 1000 * 60)
        laydate = layui.laydate;
        //日期
        laydate.render({
            elem: '#date1'
        });
        laydate.render({
            elem: '#date2'
        });
    });
});