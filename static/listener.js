$(function(){

    //####################### websocket 消息处理
    if ("WebSocket" in window) {
         //Template
        var tpl_chatItem = $("#tpl_chatItem").html();
        var curWwwPath=window.document.location.href;
        var pathName=window.document.location.pathname;
        var pos=curWwwPath.indexOf(pathName);
        var localhostPaht=curWwwPath.substring(7,pos);

        var ws = new WebSocket('ws://'+localhostPaht+'/websocket')

        ws.onmessage = function(event){

            obj = eval("("+event.data+")")

            if(obj.type=="normal"){

                var tpl = tpl_chatItem.replace("{0}", obj.message)
                        .replace("{1}", obj.avatar)
                        .replace("{3}", obj.nickname)

                if(obj.email==current_user){
                    tpl = tpl.replace("{2}", "me")
                }else{
                    tpl = tpl.replace("{2}", "you")
                }
                var $container = null;
                if( obj.from!=undefined ){

                    var from = obj.from
                    var to = obj.to
                    $container = $("#chat-"+from);
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
                        $("#chatMember").append(tpl_chatmember)
                    }

                    //更新聊天面板项
                    var length = $("#chat-"+client.id).length
                    if(length==0){
                        var tpl_chatcontainer = $("#tpl_chatcontainer").html()
                                .replace("{0}", "chat-"+client.id)
                                .replace("{1}", "与"+client.nickname+"聊天中...")
                                .replace("{2}", client.id)
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


});