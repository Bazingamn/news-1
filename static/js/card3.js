$(document).ready(function() {
    layui.use(['table'], function() {
        var table = layui.table;
        getCard3Data = function() {
            var table_data = table.render({
                elem: '#hot_news_table',
                url: '/web/getHotNews',
                cellMinWidth: 80 //全局定义常规单元格的最小宽度，layui 2.2.1 新增
                    ,
                cols: [
                    [
                        { field: '_id', title: 'ID', sort: true, width: 170 }, { field: 'read_num', title: '点击量', width: 100, sort: true },
                        { field: 'title', title: '新闻标题', width: 400 }, { field: 'from', width: 100, title: '来源' },
                        { field: 'tag', width: 70, title: '标签' }, { field: 'time', title: '发布时间', sort: true }
                    ]
                ],
            });
            table.render({
                elem: '#hot_search_table',
                url: '/web/getHotSearch',
                cellMinWidth: 80 //全局定义常规单元格的最小宽度，layui 2.2.1 新增
                    ,
                cols: [
                    [
                        { field: 'search_num', title: '搜索量', align: 'center', sort: true },
                        { field: 'keyword', align: 'center', title: '关键词'}
                    ]
                ],
                done: function() {
                    $('#hot_news_title').addClass('graph-title-item-selected')
                    $('#hot_news_title').removeClass("graph-title-item");
                    $('#hot_search_title').addClass('graph-title-item');
                    $('#hot_search_title').removeClass('graph-title-item-selected');
                    $("#hot_search_table").next().hide();
                    $("#hot_news_table").next().show();
                }
            });
        }
        getCard3Data()
        setInterval(function() {
            getCard3Data()
        }, 1000 * 60)
    })
})