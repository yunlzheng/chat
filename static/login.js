/**
 * Created by zheng on 13-10-12.
 */
$(function(){
    //#############页面初始化
    (function(){

        $.ajax({

            url: "/background",
            type: 'get',
            success: function(result){
                console.log(result);
                $("#fullscreen_post_bg").css('background-image','url('+result+')');
                $("#fullscreen_bg_load").hide();
            }

        });

    })();

    //##############页面事件处理
    (function(){

         $("form").submit(function(){
            return true;
        });

    })();

});
