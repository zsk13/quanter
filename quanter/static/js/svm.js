$(function() {
    window.onload=function(){ 
    //设置年份的选择 
        var myDate= new Date(); 
        var startYear=2000;
        var endYear=myDate.getFullYear(); 
        var obj=document.getElementById('year') 
        for (var i=startYear;i<=endYear;i++) 
        { 
            obj.options.add(new Option(i,i)); 
        } 
        obj.options[14].selected=1;

        var quarter=document.getElementById('quarter') 
        quarter.options.add(new Option('一',1));
        quarter.options.add(new Option('二',2));
        quarter.options.add(new Option('三',3));
        quarter.options.add(new Option('四',4));
    } 



})

function train(){

    var year = $("#year").val();
    var quarter = $("#quarter").val();
    $.get("/svmStrategy/training?year="+year+"&quarter="+quarter,function(data,status){
        datas = []
        codes = data['resultCode'];
        names = data['resultName'];
        console.log(typeof(codes));
        for(var i=0;i<codes.length;i++){
            datas.push({id:codes[i],name:names[i]});
        }
        $('#chosenStock').bootstrapTable({
        striped: true,
        sidePagination: "client",
        pageNumber: 1,
        pageSize: 10,
        pageList: [10, 25, 50, 100],
        height: 400,
        clickToSelect: true,
        columns: [{
            field: 'id',
            title: '股票代码'
        }, {
            field: 'name',
            title: '股票名称'
        }],
        // data: stocks
        data: datas
        
    });
    }); 
   
}

function test(){ 
    var start = $("#start").val();
    var end = $("#end").val();
    var code = $("#code").val();

    var myChart = echarts.init(document.getElementById('TestResult'));
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
                    
    $(window).resize(function() {
        myChart.resize()
    });
    myChart.setOption(option)
}