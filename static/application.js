$(function(){

    //emoji config
    emojify.setConfig({
        emojify_tag_type: 'img',
        emoticons_enabled: true,
        people_enabled: true,
        nature_enabled: true,
        objects_enabled: true,
        places_enabled: true,
        symbols_enabled: true
    });

    //初始化emoji表情
    emojify.run();

    //##############################页面初始化
    var tpl_chatcontainer = $("#tpl_chatcontainer").html()
            .replace("{0}", "all")
            .replace("{1}", "群聊中")
    $("#chat_containers").empty().append(tpl_chatcontainer)
    $("#all").fadeIn(500);

    //################################ 用户列表点击处理
    $("#chatMember").delegate(".chatListColumn","click", function(){

        var target = $(this).attr("target");
        if(target!=undefined){
            var _class = $(target).attr("class")
            $("."+_class).hide();
            $(target).fadeIn(500);
        }

    });

    //############################## 表情支持
    $(".btn_face").click(function(e){

        var xx = (e.pageX || e.clientX + document.body.scrollLeft)-290;
        var yy = (e.pageY || e.clientY + document.boyd.scrollTop)-155;
        $("#emoji_face").css("top",yy).css("left",xx).toggle();

    });

    $("#emoji_face").delegate("li", "click", function(e){

        var emoji = $($(this).find('img')[0]).attr('title');
        tmp = $("#textInput").val()+emoji
        $("#textInput").val(tmp);
        emojify.run();

    });

    //##################################### 发送信息
    $("body").on('click', '.chatSend', function(){

        var $from = $(this).parent('form')
        $from.submit()
        return false

    });

    //ctrl+Enter发送信息
    $("#textInput").keyup(function(e){

        if(e.ctrlKey && e.which == 13 || e.which == 10) { // Ctrl+Enrer(回车)
             //需要执行的代码
            $("#btnSend").click();
        }

    });

    $("body").delegate('.sendForm', 'submit', function(){

        var $textarea = $(this).find('textarea')
        var $input = $(this).find('input')
        var message = $textarea.val()
        var to = $input.val();
        to = to=='{2}'?'':to;
        $.post("./chat", { data: message, to: to }, function(data){
            $("#data").val('');
        });
        $textarea.val("");
        return false;

    });

});