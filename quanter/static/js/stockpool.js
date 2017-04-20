$(function() {
    var dataarray = []

    window.actionEvents = {
        'click .delete' : function(e, value, row, index) {
            console.log(index);
            console.log(dataarray);
            code = dataarray.splice(index,1);

            code = code[0].id;
            console.log(dataarray);
            $('#tablePool').bootstrapTable("load",dataarray);
            $.get("/stockpool/deleteStock?code="+code,function(data,status){
                console.log(data);
            })

        }
    }

    for(var d in list){
        var temp = {}
        temp.id = list[d]
        dataarray.push(temp)
    }
    $('#tablePool').bootstrapTable({
        striped: true,
        sidePagination: "client",
        pageNumber: 1,
        pageSize: 10,
        pageList: [10, 25, 50, 100],

        clickToSelect: true,
        columns: [{
            field: 'id',
            title: '股票代码',
            width: 200,
        }, {
            field: 'action',
            title: '操作',
            formatter :"<a class='delete'>删除</a>",
            events : "actionEvents",
            width: 200,
        }],
        data: dataarray
    })

});

