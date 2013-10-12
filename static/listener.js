$(function(){

    //#################### 消息提醒模块
    (function(){

        var snd = new Audio("/static/mp3/notification.mp3"); // buffers automatically when created

        $(window).on('message', function(event, data){

            if(data.email==current_user){

                //自己的消息不提醒
                return;

            }else{

                console.log(data);
                //显示未读消息的条数
                var $target = $(".chatContainer[data-main='"+data.email+"']");

                if((data.to_email==current_user) && ($target.is(":visible")==false)){

                    var $list_target = $(".chatListColumn[data-target='"+data.email+"']");
                    var $info = $list_target.find('.label-info');
                    var num =parseInt( $info.html())+1;
                    $info.show().html(num);


                }

                if((data.to_email=='groups') && ($("#all").is(':visible')==false)){

                   var $info = $("#chat-all").find('.label-info');
                   var num =parseInt( $info.html())+1;
                   $info.show().html(num);

                }

                 //调用html5 audio播放提示音
                 var hasVideo = !!(document.createElement('video').canPlayType);
                 if(hasVideo==true){
                     //播放提示音
                     snd.play();

                 }

                 //调用webkitNotifications
                 if(window.webkitNotifications){
                     //浏览器功能检测
                     //console.log("Notifications are supported!");
                     if (window.webkitNotifications.checkPermission() == 0) {

                         var notification = window.webkitNotifications.createNotification(
                                data.avatar, data.nickname+ '发来了新消息', data.message);
                         notification.show();
                         notification.onclick=function(){

                             //页面显示聊天面板
                             var $target = $(".chatContainer[data-main='"+data.email+"']");
                             if(data.to==''){
                                 $target = $(".chatContainer[data-main='groups']");
                             }
                             var _class = $target.attr("class")
                             $("."+_class).hide();//隐藏其他面板
                             $target.fadeIn(1000);
                             //聚焦浏览器
                             $(window).focus();

                         };
                         window.setTimeout(function(){

                            notification.cancel();

                         }, 5000);

                     }else{
                         window.webkitNotifications.requestPermission();
                     }

                 }

            }

        });

    })();

    //####################### websocket 消息处理
    (function(){

         if ("WebSocket" in window) {

             //Template
            var tpl_chatItem = $("#tpl_chatItem").html();
            var curWwwPath=window.document.location.href;
            var pathName=window.document.location.pathname;
            var pos=curWwwPath.indexOf(pathName);
            var localhostPaht=curWwwPath.substring(7,pos);

            var ws = new WebSocket('ws://'+localhostPaht+'/websocket')

            ws.onmessage = function(event){

                var obj = eval("("+event.data+")")

                if(obj.type=="normal"){

                    $(window).trigger("message", obj);

                    var tpl = tpl_chatItem.replace("{0}", obj.message)
                            .replace("{1}", obj.avatar)
                            .replace("{3}", obj.nickname)

                    if(obj.email==current_user){
                        tpl = tpl.replace("{2}", "me")
                    }else{
                        tpl = tpl.replace("{2}", "you")
                    }
                    var $container = null;
                    if( obj.from != undefined ){

                        var to = obj.to
                        var from_email = obj.email;//发送用户邮箱

                        //更新页面编号
                        /*说明 如果是给我发送的消息，
                         但是我当前的client编号和to编号不一致，
                         则说明我刷新的页面,此时需要更新我的
                       */
                        $container = $(".chatContainer[data-main='"+from_email+"']");

                        if(obj.email==current_user){
                            $container = $("#chat-" + to);
                        }

                    }else{
                        $container = $("#all")
                    }

                    var $scroll = $container.find(".chatScorll");
                    $scroll.append(tpl);
                    $scroll.scrollTop($scroll[0].scrollHeight);

                    emojify.run();

                }else if(obj.type=="add"){
                    /**
                     * bugs:
                     * 当其他用户刷新页面后 会出现多个聊天面板  data-main='email'相同[修改判断参数为聊天面板email]
                     *
                     * */

                    for(var i=0;i<obj.clients.length;i++){

                        //更新用户列表项
                        //有新成员加入
                        var client = obj.clients[i]
                        var length = $("#"+client.id).length
                        if(length==0){
                            var tpl_chatmember = $("#tpl_chatmember").html()
                                .replace("{0}", client.avatar)
                                .replace("{1}", client.nickname)
                                .replace("{2}", "")
                                .replace("{3}", client.id)
                                .replace("{4}", client.id)
                                .replace("{5}", client.email);
                            $("#chatMember").append(tpl_chatmember)
                        }

                        //更新聊天面板项
                        //var length = $("#chat-"+client.id).length
                        var length = $(".chatContainer[data-main='"+client.email+"']").length;
                        if(length==0){

                            var tpl_chatcontainer = $("#tpl_chatcontainer").html()
                                    .replace("{0}", "chat-"+client.id)
                                    .replace("{1}", "与"+client.nickname+"聊天中...")
                                    .replace("{2}", client.id)
                                    .replace("{3}", client.email);
                            $("#chat_containers").append(tpl_chatcontainer)

                        }

                    }

                }else if(obj.type=='out'){
                    var select = "#"+obj.id;
                    $(select).fadeOut(1000).remove();
                }
            }

        } else {

            alert("WebSocket not supported");

        }

    })();

});