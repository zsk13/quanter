function addStock(){
    var code = $("#code").val();
    $.get("/stockpool/addStock?code="+code,function(data,status){
        console.log(data);
    })
}


