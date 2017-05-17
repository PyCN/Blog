$(document).ready(function(){
    $(document).ajaxStart(function() {
        console.log(arguments)
    }).ajaxComplete(function() {
           console.log(arguments);
       });
     $(document).ajaxError(function (event, jsXHR, settings, errorType) {  
    //第一个参数（事件对象）  
    console.log(event.type); //打印出：ajaxError    即：触发的事件  
    console.log(event.target); //打印出：[object HTMLDocument]   即：触发事件的元素  

    //第二个参数  
    console.log(jsXHR.statusText);  //第二个参数是一个XMLHttpRequst对象  

    //第三个参数  详情请参照http://www.w3school.com.cn/jquery/ajax_ajax.asp  
    for (var a in settings) {  
        console.log(a + "<br/>") //通过打印得知：其实这个settings就是本次AJAX请求的所有参数设置：详情如下  
        /* 
        url              注意：settings是一个对象。以下都是这个对象的属性或者方法 
        type 
        isLocal 
        global 
        processData 
        async 
        contentType 
        accepts 
        contents 
        responseFields 
        converters 
        flatOptions 
        xhr 
        jsonp 
        jsonpCallback 
        success 
        dataTypes 
        crossDomain 
        hasContent 
        */  
    }  

    console.log(settings.url); //打印出：loadHandler.ashx?id=v  即：发生错误的请求url  
    console.log(settings.type);//打印出：GET   即：发生错误的请求的请求方式  
    console.log(settings.global) //打印出：true 即：是否触发全局 AJAX 事件。默认值: true。设置为 false 将不会触发全局 AJAX 事件，如 ajaxStart 或 ajaxStop 可用于控制不同的 Ajax 事件  

    console.log(settings.async); //打印出：true 即请求为异步。 如果是false 表示请求为同步  
    console.log(settings.dataTypes); //打印出：text,html  即：预期服务器返回的数据类型。如果不指定，jQuery 将自动根据 HTTP 包 MIME 信息来智能判断 */  

    for (var b in settings.contents) {  //contents是一个对象  
        console.log(b + "<br/>")  //打印出： xml, html,json,script  
    }  

    //第四个参数 （错误描述）  
    console.log(errorType); //打印出：Internal Server Error :即发生错误的类型 ，内部服务器错误  
}) 
});