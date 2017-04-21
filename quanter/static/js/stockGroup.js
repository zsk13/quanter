var dataarray = []
$(function() {
    window.actionEvents = {
        'click .delete' : function(e, value, row, index) {
            console.log(index);
            console.log(dataarray);
            group = dataarray.splice(index,1);

            id = group[0].id;
            console.log(dataarray);
            $('#stockGroup').bootstrapTable("load",dataarray);
            $.get("/stockGroup/deleteStockGroup?groupId="+id,function(data,status){
                console.log(data);
            })

        }
    }

    $.get("/stockGroup/getStockGroups",function(data,status){
        console.log(data);
        dataarray = data


        $('#stockGroup').bootstrapTable({
            striped: true,
            sidePagination: "client",
            pageNumber: 1,
            pageSize: 10,
            pageList: [10, 25, 50, 100],

            clickToSelect: true,
            columns: [{
                field: 'groupName',
                title: '股票组名称',
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

    })

});

function addStockGroup(){
    var groupName = $("#groupName").val();
    $.get("/stockGroup/addStockGroup?groupName="+groupName,function(data,status){
        dataarray.push(data);
        $('#stockGroup').bootstrapTable("load",dataarray);
    })
}