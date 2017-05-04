$(function() {
    $.get("/stockGroup/getStockGroups",function(data,status){
        console.log("showStock");
        console.log(data);
        for(var d in data){
            $("#stockGroupsUL").append("<li><a onclick = addStock("+data[d].id+")>"+data[d].groupName+"</a></li>");
        }
    })
})

function addStock(groupId){
    var code = $("#code").val();
    $.get("/stockGroup/addStock?groupId="+groupId+"&code="+code,function(data,status){

    })
}