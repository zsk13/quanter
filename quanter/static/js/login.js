$(function () {
     $.get("/logininfo",function(data,status){
        if( data == "unexist"){
            $("#login").css("display","inline");
        }else{
            $("#login").css("display","none");
            $("#user").text(data);
        }
        
     })

}
)