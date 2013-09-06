$(document).ready(function(){
    $('textarea[name="context"]').blur(function(){
        context_judge($('textarea[name="context"]').val());
    });
    $('input[name="image"]').blur(function(){
        image_judge($('input[name="image"]').val());
    });
    window.image = true;
    $('#upload_button').click(function(){
        if(window.context && window.image){
            $('#upload_form').submit();
        }
        else{
            context_judge($('textarea[name="context"]').val());
            image_judge($('input[name="image"]').val());
        }
    });
});

function context_judge(context){
    if (context == ''){
        result_display('context', '0', '文字内容不能为空');
        window.context = false;
    }
    else if (context.length > 300){
        result_display('context', '0', '文字内容不能超过300个字符');
        window.context = false;
    }
    else{
        result_display('context', '1', '');
        window.context = true;
    }
}

function image_judge(image){
    result_display('image', '1', '');
    window.image = true;
}

function result_display(object, result, text){
    if (result == '1'){
        result_html = '<img src="/image/tick.png"/><div>' + text + '</div>';
    }
    else{
        result_html = '<img src="/image/cross.png"/><div>' + text + '</div>';
    }
    $('#' + object + '_judge_div').html(result_html);
}
