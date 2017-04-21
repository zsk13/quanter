$(function() {
    $.get("/stockGroup/getStockGroups",function(data,status){
        console.log("showStock");
        console.log(data);
        for(var d in data){
           $("#stockGroupsForTest").append("<option value='"+data[d].id+"'>"+data[d].groupName+"</option>"); 
        }
    })
}
)