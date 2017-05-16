$(function() {
    $("#breach").val(paraList['breach']);
    for(var i = 0;i<stockGroups.length;i++){
        $("#selectGroup").append("<option value="+stockGroups[i]['id']+">"+stockGroups[i]['name']+"</option>");
    }

    var myChart = echarts.init(document.getElementById('kline'));
    var dates = rawData.map(function(item) {
            return item[0]
            });
    var profits = rawData.map(function(item) {
            return item[1]
            });

    var option = {
        tooltip: {
                trigger: 'axis'
            },
        legend: {
                data:['持有现值（元）']
            },
        grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
        toolbox: {
                feature: {
                    saveAsImage: {}
                }
            },
        xAxis: {
                type: 'category',
                boundaryGap: false,
                data: dates
            },
        yAxis: {
                type: 'value'
            },
        series: [
                {
                    name:'持有现值（元）',
                    type:'line',
                    data:profits
                },
            ]
        };
    $(window).resize(function() {
        myChart.resize()
    });
    myChart.setOption(option);
});

function addInputStock(){
    st_code = $('#st_code').val();
    $.get("/gap/findStock?st_code="+st_code,function(data,status){
        st_info = data['st_info']
        newstocks = []
        newstocks.push({id:st_info['code'],name:st_info['name']})
        $('#tablepool').bootstrapTable('append', newstocks)
    })
}
function filterStocks(){
    var groupId = $("#selectGroup").val()
    var startDate = $("#start").val()
    var endData = $("#end").val()
    var breach = $("#breach").val()

    //加载icon
    var opts = {
      lines: 13 // The number of lines to draw
    , length: 28 // The length of each line
    , width: 14 // The line thickness
    , radius: 42 // The radius of the inner circle
    , scale: 1 // Scales overall size of the spinner
    , corners: 1 // Corner roundness (0..1)
    , color: '#000' // #rgb or #rrggbb or array of colors
    , opacity: 0.25 // Opacity of the lines
    , rotate: 0 // The rotation offset
    , direction: 1 // 1: clockwise, -1: counterclockwise
    , speed: 1 // Rounds per second
    , trail: 60 // Afterglow percentage
    , fps: 20 // Frames per second when using setTimeout() as a fallback for CSS
    , zIndex: 2e9 // The z-index (defaults to 2000000000)
    , className: 'spinner' // The CSS class to assign to the spinner
    , top: '50%' // Top position relative to parent
    , left: '50%' // Left position relative to parent
    , shadow: false // Whether to render a shadow
    , hwaccel: false // Whether to use hardware acceleration
    , position: 'absolute' // Element positioning
    }
    var target = document.getElementById('table')
    var spinner = new Spinner(opts).spin(target);

    $.get("/gap/filterStocks?start="+start+"&end="+end+"&breach="+breach+"&groupId="+groupId,function(data,status){
        spinner.spin();
        recommendData_new = data['recommendData'];
        $('#table').bootstrapTable('load', recommendData_new)
    });


}
function addStocks(){
    selected_list = $('#table').bootstrapTable('getSelections');
    newstocks = []
    for (var i=0;i<selected_list.length;i++)
    {
        newstocks.push({id:selected_list[i].id,name:selected_list[i].name});
    }

    $('#tablepool').bootstrapTable('append', newstocks)

}

function backTest(){
    var startDate = $("#start").val()
    var endDate = $("#end").val()
    var iniMoney = $("#ini_money").val()
    var breach = $("#breach").val()

    var stocks = $('#tablepool').bootstrapTable('getData');
    var idList = []
    for (var i=0;i<stocks.length;i++)
    {
        idList.push(stocks[i].id);
    }

    //加载icon
    var opts = {
      lines: 13 // The number of lines to draw
    , length: 28 // The length of each line
    , width: 14 // The line thickness
    , radius: 42 // The radius of the inner circle
    , scale: 1 // Scales overall size of the spinner
    , corners: 1 // Corner roundness (0..1)
    , color: '#000' // #rgb or #rrggbb or array of colors
    , opacity: 0.25 // Opacity of the lines
    , rotate: 0 // The rotation offset
    , direction: 1 // 1: clockwise, -1: counterclockwise
    , speed: 1 // Rounds per second
    , trail: 60 // Afterglow percentage
    , fps: 20 // Frames per second when using setTimeout() as a fallback for CSS
    , zIndex: 2e9 // The z-index (defaults to 2000000000)
    , className: 'spinner' // The CSS class to assign to the spinner
    , top: '50%' // Top position relative to parent
    , left: '50%' // Left position relative to parent
    , shadow: false // Whether to render a shadow
    , hwaccel: false // Whether to use hardware acceleration
    , position: 'absolute' // Element positioning
    }
    var target = document.getElementById('kline')
    var spinner = new Spinner(opts).spin(target);
    $.get("/gap/backTest?start="+start+"&end="+end+"&iniMoney="+iniMoney+"&breach="+breach+"&idList="+idList,function(data,status){
        spinner.spin();
        rawData = data['profitRate_day'];
        var myChart = echarts.init(document.getElementById('kline'));
        var dates = rawData.map(function(item) {
            return item[0]
        });
        var profits = rawData.map(function(item) {
            return item[1]
        });
        //alert(profits)
        var option = {
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data:['持有现值（元）']
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            toolbox: {
                feature: {
                    saveAsImage: {}
                }
            },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data: dates
            },
            yAxis: {
                type: 'value'
            },
            series: [
                {
                    name:'持有现值（元）',
                    type:'line',
                    data:profits
                },
            ]
        };
        $(window).resize(function() {
            myChart.resize()
        });
        myChart.setOption(option);
    });
}
