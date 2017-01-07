$(document).ready(function(){
    $("#search").css("backgroud-color", "red").slideUp(1000).slideDown(1000);
    $('input.generate_qrcode').click(submit_qrcode);
    $('input.praise').click(praise);
});
function submit_qrcode(){
    var target_url = $('input[name=target_url]').val();
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
};

function praise(){
    var target_url = $(this).attr('href');
    var likes = $(this).next()
    $.ajax({
        type: "GET",
        url: target_url,
        dataType: 'json',
        success: function(data){
            var error_code = data.error_code;
            var likes_num = data.likes;
            if (error_code == 0)
                likes.text(likes_num);
            else if (error_code == -3)
                alert('您已赞过');
            //var dictdata = $.parseJSON(data);
            //console.log(dictdata.error_code);
        },
        error: function(data){
            alert("登陆后才可点赞");
        }
    });
}