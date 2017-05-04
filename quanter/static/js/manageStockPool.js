function addStock(){
    var code = $("#code").val();
    $.get("/stockGroup/addStock?code="+code,function(data,status){
        console.log(data);
    })
}


$(function() {
    $.get("/stockGroup/getStockGroups",function(data,status){
        console.log("showStock");
        console.log(data);
        for(var d in data){
            $("#groupsUL").append("<li><a href = '/stockGroup/showStockGroup?groupId="+data[d].id+"'>"+data[d].groupName+"</a></li>");
        }
    })
})