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

                $("#fullscreen_post_bg").hide().css('background-image','url('+result+')').fadeIn(500);
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
