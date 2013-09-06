$(document).ready(function(){
    $('input[name="username"]').blur(function(){
        username_judge($('input[name="username"]').val());
    });
    $('input[name="password"]').blur(function(){
        password_judge($('input[name="password"]').val());
    });
    $('input[name="captcha_1"]').blur(function(){
        captcha_judge($('input[name="captcha_0"]').val(), $('input[name="captcha_1"]').val());
    });
    $('#login_button').click(function(){
        if(window.username && window.password && window.captcha){
            $('#login_form').submit();
        }
        else{
            username_judge($('input[name="username"]').val());
            password_judge($('input[name="password"]').val());
            captcha_judge($('input[name="captcha_0"]').val(), $('input[name="captcha_1"]').val());
        }
    });
    $('.captcha').click(function(){
        $.get('/account/captcha_refresh/', function(result){
            json_result = eval('(' + result + ')');
            if (json_result.state == '1'){
            	$('.captcha').attr('src', json_result.new_captcha_image);
            	$('#id_captcha_0').val(json_result.new_captcha_hashkey);
            }
        });
    });
});

function username_judge(username){
    if (username == ''){
        result_display('username', '0', '用户名不能为空');
        window.username = false;
    }
    else{
        result_display('username', '1', '');
        window.username = true;
    }
}

function password_judge(password){
    if (password == ''){
        result_display('password', '0', '密码不能为空');
        window.password = false;
    }
    else{
        result_display('password', '1', '');
        window.password = true;
    }
}

function captcha_judge(captcha_0, captcha_1){
	if (captcha_1 == ''){
        result_display('captcha', '0', '验证码不能为空');
        window.captcha = false;
    }
    else{
    	$.get('/account/captcha_judge/?captcha_0=' + captcha_0 + '&captcha_1=' + captcha_1, function(result){
            json_result = eval('(' + result + ')');
            if (json_result.state == '1'){
                result_display('captcha', '1', '');
                window.captcha = true;
            }
            else if (json_result.state == '2'){
                result_display('captcha', '0', '验证码错误');
                window.captcha = false;
            }
        });
    }
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
