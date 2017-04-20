function findParam(){
    var start = $("#start").val();
    var end = $("#end").val();
    var code = $("#code").val();
    var m = $("#m").val();
    var n = $("#n").val();
    $.get("/maStrategy/autoFindParam?code="+code+"&start="+start+"&end="+end+"&m="+m+"&n="+n,function(data,status){

        console.log(data);
        dataarray = []
        for(var d in data){
            d = data[d]
            var temp = {}
            temp.n = d[0]
            temp.m = d[1]
            temp.ratio = Number(d[2]*100).toFixed(2)+'%'
            dataarray.push(temp)
        }

        $('#autoTestTable').bootstrapTable({
        striped: true,
        sidePagination: "client",
        pageNumber: 1,
        pageSize: 10,
        pageList: [10, 25, 50, 100],
        clickToSelect: true,
        columns: [{
            field: 'n',
            title: 'n',
            width:200
        }, {
            field: 'm',
            title: 'm',
            width:200
        }, {
            field: 'ratio',
            title: '收益率',
            width:200
        }],
        data: dataarray
    })
    });
}

// $(function() {
//     $('#autoTestTable').bootstrapTable({
//         striped: true,
//         sidePagination: "client",
//         pageNumber: 1,
//         pageSize: 10,
//         pageList: [10, 25, 50, 100],
//         clickToSelect: true,
//         columns: [{
//             field: 'n',
//             title: 'n',
//             width: 200
//         }, {
//             field: 'm',
//             title: 'm',
//             width: 200
//         }, {
//             field: 'ratio',
//             title: '收益率',
//             width: 200
//         }],

//         data: [{
//             n: '2',
//             m: '3',
//             field : '0.1'
//         }, {
//             n: '2',
//             m: '3',
//             field : '0.1'
//         }]
//     })
// });