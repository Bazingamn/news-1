$(document).ready(function() {
    layui.use(['layer'], function() {
        var geoCoordMap = {};

        var convertData = function(data) {
            var res = [];
            for (var i = 0; i < data.length; i++) {
                var geoCoord = geoCoordMap[data[i].name];
                if (geoCoord) {
                    res.push(geoCoord.concat(data[i].name).concat(data[i].value));
                }
            }
            return res;
        };

        optionMap = {
            title: {
                text: '',
                left: 'center',
                textStyle: {
                    color: '#fff'
                }
            },
            backgroundColor: '#FFF',
            visualMap: {
                min: 0,
                max: 500,
                splitNumber: 5,
                inRange: {
                    color: ['#d94e5d', '#eac736', '#50a3ba'].reverse()
                },
                textStyle: {
                    color: '#000'
                }
            },
            geo: {
                map: 'china',
                label: {
                    emphasis: {
                        show: true,
                        color: '#009688',
                        textStyle: {
                            color: '#000'
                        }
                    },
                    normal: {
                        show: false,
                    },
                },
                roam: false,
                itemStyle: {
                    normal: {
                        areaColor: '#FFF',
                        borderColor: '#009688'
                    },
                    emphasis: {
                        areaColor: '#79C2D6',
                        shadowColor: 'rgba(121,194, 214, 0.5)',
                        shadowBlur: 10
                    }
                }
            },

            series: [{
                roam:false,
                name: '访问量',
                type: 'scatter',
                coordinateSystem: 'geo',
                data: convertData([])
            }],
            //官方实例tooltip
            tooltip: {
                trigger: 'item',
                backgroundColor: 'rgba(0,0, 0, 0.5)',
                formatter: function(params) { //格式化鼠标移上去显示内容样式
                    return '城市：' + params.value[2] + '<br/>访问量：' + params.value[3]
                }
            },
        };
        //初始化echarts实例
        var mapChart = echarts.init(document.getElementById('heatmap'));

        mapChart.setOption(optionMap);
        //使用制定的配置项和数据显示图表
        $.ajax({
            url: '/web/getUseLoc/',
            success: function(res) {
                if (res.code == 0) {
                    geoCoordMap = res.data.geo_map
                    optionMap.series[0].data = convertData(res.data.count_data)
                    optionMap.visualMap.max = res.data.max
                    mapChart.clear()
                    mapChart.setOption(optionMap);
                } else {
                    parent.layer.msg(res.data, { time: 500 })
                }
            },
            fail: function(res) {
                console.log(res)
            }
        })
    })
})
// console.log(res)
// if (res.code == 0) {
//     geoCoordMap=res.data.geo_map
//     optionMap.series[0].data= convertData([res.data.count_data])
//     optionMap.visualMap.max=res.data.max
//     console.log(geoCoordMap)
//     console.log(optionMap)
//     mapChart.setOption(optionMap);
// } else {
//     parent.layer.msg(res.data, { time: 500 })
// }