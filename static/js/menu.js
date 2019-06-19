layui.use(['layer', 'element'], function() {
    var element = layui.element; //导航的hover效果、二级菜单等功能，需要依赖element模块
    var $ = layui.jquery
    //监听导航点击
    element.on('nav(nav)', function(elem) {
        // layer.msg(elem.text());
        if (elem[0].dataset.page == 'logout') {
            layer.confirm('确定退出？', {
                btn: ['是', '否'], //可以无限个按钮
            }, function(index, layero) {
                //按钮【按钮一】的回调
                window.location.href = '/web/logout/'
            });
        } else {
            var loading = layer.load(0, {
                shade: false,
                time: 1000
            });
            var html='<iframe class="right" target="tab"  id="tabframe" frameborder="no" border="0"  src="'+elem[0].dataset.page+'"></iframe>'
            var id=new Date().getTime()
            element.tabAdd('tabList', {
                title: elem.text(),
                content: html,
                id:id
            });
            element.tabChange('tabList',id); 
        }
    });
    $('.site-demo-active').on('click', function() {
        var othis = $(this),
            type = othis.data('type');
        active[type] ? active[type].call(this, othis) : '';
    });

    //Hash地址的定位
    var layid = location.hash.replace(/^#test=/, '');
    element.tabChange('test', layid);

    element.on('tab(test)', function(elem) {
        location.hash = 'test=' + $(this).attr('lay-id');
    });
});