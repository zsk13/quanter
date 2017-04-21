function train(){
    var start = $("#start").val();
    var end = $("#end").val();
    var code = $("#code").val();
    var verifystart = $("#verifystart").val();
    var verifyend = $("#verifyend").val();
    var groupId = $("#stockGroupsForTest").val();
    $.get("/svmStrategy/result?code="+code+"&start="+start+"&end="+end+"&verifystart="+verifystart+"&verifyend="+verifyend+"&groupId="+groupId,function(data,status){

        console.log(data);
        dataarray = []
        for(var d in data){
            d = data[d]
            var temp = {}
            temp.code = d[0]
            temp.ratio = Number(d[1]*100).toFixed(2)+'%'
            dataarray.push(temp)
        }

        $('#testResult').bootstrapTable({
        striped: true,
        sidePagination: "client",
        pageNumber: 1,
        pageSize: 10,
        pageList: [10, 25, 50, 100],
        clickToSelect: true,
        columns: [{
            field: 'code',
            title: 'code',
            width:200
        }, {
            field: 'ratio',
            title: '收益率',
            width:200
        }],
        data: dataarray        
        });
        $('#testResult').bootstrapTable("load",dataarray);
    }); 
   
}
