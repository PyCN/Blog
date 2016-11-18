$(document).ready(function(){
    $("#search").css("backgroud-color", "red").slideUp(1000).slideDown(1000);
    $('input.generate_qrcode').click(submit_qrcode);
});
function submit_qrcode(){
    target_url = $('input[name=target_url]').val();
    if (target_url == ''){
        target_url = document.URL
    }
    $.post(
        '/qrcode', 
        {'target_url': target_url},
        function(result){
            var tooltip = "<div id='tooltip'><img class='qrcode' title='点击关闭二维码' alt='生成二维码'><\/div>";
            $("body").append(tooltip);	//把它追加到文档中	
            // 直接获取图片数据流，base64编码
            $('img.qrcode').attr("src", "data:image/png;base64," + result);			 
            $("#tooltip")
                    .css({
                        "top": "100px",
                        "left":  "500px"
                    }).show("fast");
            $("#tooltip").click(function(){$("#tooltip").remove();});
            })
}