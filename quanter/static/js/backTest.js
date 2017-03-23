Date.prototype.format = function(fmt)     
{ //author: meizz     
  var o = {     
    "M+" : this.getMonth()+1,                 //月份     
    "d+" : this.getDate(),                    //日     
    "h+" : this.getHours(),                   //小时     
    "m+" : this.getMinutes(),                 //分     
    "s+" : this.getSeconds(),                 //秒     
    "q+" : Math.floor((this.getMonth()+3)/3), //季度     
    "S"  : this.getMilliseconds()             //毫秒     
  };     
  if(/(y+)/.test(fmt))     
    fmt=fmt.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length));     
  for(var k in o)     
    if(new RegExp("("+ k +")").test(fmt))     
  fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length)));     
  return fmt;     
}    

function getOption(dateData,yieldRateData,standardData){
    dates = [];
    for(var value in dateData){
        dates.push(new Date(dateData[value]).format("yyyy-MM-dd"));
    }

    option = {
        title : {
            text: 'backtest',
        },
        tooltip : {
            trigger: 'axis',
        },
        legend: {
            data:['策略收益','基准收益']
        },
        toolbox: {
            show : true,
            feature : {
                mark : {show: true},
                dataView : {show: true, readOnly: false},
                magicType : {show: true, type: ['line', 'bar', 'stack', 'tiled']},
                restore : {show: true},
                saveAsImage : {show: true}
            }
        },
        calculable : true,
        xAxis : [
            {
                type : 'category',
                boundaryGap : false,
                data : dates,

            }
        ],
        yAxis : [
            {
                type : 'value',
                axisLabel : {
                    formatter: function (value, index) {
                        var str=Number(value*100).toFixed(2);
                        str+="%";
                        return str;
                    },
                },
                
            }
        ],

        series : [
            {
                name:'策略收益',
                type:'line',
                stack: '总量',
                data:  yieldRateData,
            },

            {
                name:'基准收益',
                type:'line',
                stack: '总量',
                data:  standardData,
            },
        ]
    };
    return option;
}

$(function() {
    var myChart = echarts.init(document.getElementById('backTest'));
    if(typeof(dateData)=="undefined"){ 
        return;
    } 
    console.log(dateData);
    console.log(yieldRateData);
    console.log(standardData);
    dateData = dateData['index'];
    yieldRateData = yieldRateData['data'];
    standardData = standardData['data'];
    
    option = getOption(dateData,yieldRateData,standardData);      
    $(window).resize(function() {
        myChart.resize()
    });
    myChart.setOption(option)
});

function check(){ 
    var start = $("#start").val();
    var end = $("#end").val();
    var code = $("#code").val();
    $.get("/backTest/?code="+code+"&start="+start+"&end="+end,function(data,status){
        var myChart = echarts.init(document.getElementById('backTest'));
        console.log(data);
        dateData = data['dateData'];
        yieldRateData = data['yieldRateData'];
        standardData = data['standardData'];
        dateData = JSON.parse(dateData);
        yieldRateData = JSON.parse(yieldRateData);
        standardData = JSON.parse(standardData);

        dateData = dateData['index'];
        yieldRateData = yieldRateData['data'];
        standardData = standardData['data'];
        option = getOption(dateData,yieldRateData,standardData);      
        $(window).resize(function() {
            myChart.resize()
        });
        myChart.setOption(option)
    });


    // var myChart = echarts.init(document.getElementById('backTest'));

    //     dateDate = data['dateData'];
    //     yieldRateData = data['yieldRateData'];
    //     standardData = data['standardData'];
    //     console.log(dateData);
    //     console.log(yieldRateData);
    //     console.log(standardData);
    //     dateData = dateData['index'];
    //     yieldRateData = yieldRateData['data'];
    //     standardData = standardData['data'];
    //     dates = [];
    //     for(var value in dateData){
    //         dates.push(new Date(dateData[value]).format("yyyy-MM-dd"));
    //     }

    //     option = {
    //         title : {
    //             text: 'backtest',
    //         },
    //         tooltip : {
    //             trigger: 'axis',
    //         },
    //         legend: {
    //             data:['策略收益','基准收益']
    //         },
    //         toolbox: {
    //             show : true,
    //             feature : {
    //                 mark : {show: true},
    //                 dataView : {show: true, readOnly: false},
    //                 magicType : {show: true, type: ['line', 'bar', 'stack', 'tiled']},
    //                 restore : {show: true},
    //                 saveAsImage : {show: true}
    //             }
    //         },
    //         calculable : true,
    //         xAxis : [
    //             {
    //                 type : 'category',
    //                 boundaryGap : false,
    //                 data : dates,

    //             }
    //         ],
    //         yAxis : [
    //             {
    //                 type : 'value',
    //                 axisLabel : {
    //                     formatter: function (value, index) {
    //                         var str=Number(value*100).toFixed(2);
    //                         str+="%";
    //                         return str;
    //                     },
    //                 },
                    
    //             }
    //         ],

    //         series : [
    //             {
    //                 name:'策略收益',
    //                 type:'line',
    //                 stack: '总量',
    //                 data:  yieldRateData,
    //             },

    //             {
    //                 name:'基准收益',
    //                 type:'line',
    //                 stack: '总量',
    //                 data:  standardData,
    //             },
    //         ]
    //     };

    //     $(window).resize(function() {
    //         myChart.resize()
    //     });
    //     myChart.setOption(option)
} 