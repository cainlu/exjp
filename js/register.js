$(document).ready(function(){
    $('input[name="username"]').blur(function(){
        username_judge($('input[name="username"]').val());
    });
    $('input[name="nickname"]').blur(function(){
        nickname_judge($('input[name="nickname"]').val());
    });
    $('input[name="password"]').blur(function(){
        password_judge($('input[name="password"]').val());
    });
    $('input[name="password2"]').blur(function(){
        password2_judge($('input[name="password"]').val(), $('input[name="password2"]').val());
    });
    $('input[name="email"]').blur(function(){
        email_judge($('input[name="email"]').val());
    });
    $('#register_button').click(function(){
    	if(window.username && window.nickname && window.password && window.password2 && window.email){
    	    $('#register_form').submit();
    	}
    	else{
    		username_judge($('input[name="username"]').val());
    		nickname_judge($('input[name="nickname"]').val());
    		password_judge($('input[name="password"]').val());
    		password2_judge($('input[name="password"]').val(), $('input[name="password2"]').val());
    		email_judge($('input[name="email"]').val());
    	}
    });
});

function username_judge(username){
	if (username == ''){
		result_display('username', '0', '用户名不能为空');
		window.username = false;
	}
	else if (username.length > 10){
        result_display('username', '0', '用户名不能超过10个字符');
        window.username = false;
    }
	else{
        $.get('/account/username_judge/?username=' + username, function(result){
            json_result = eval('(' + result + ')');
            if (json_result.state == '1'){
                result_display('username', '1', '');
                window.username = true;
            }
            else if (json_result.state == '2'){
                result_display('username', '0', '当前用户名已存在');
                window.username = false;
            }
            else if (json_result.state == '3'){
                result_display('username', '0', '相同ip24小时只能注册一次');
                window.username = false;
            }
        });
	}
}

function nickname_judge(nickname){
    if (nickname == ''){
        result_display('nickname', '0', '昵称不能为空');
        window.nickname = false;
    }
    else if (nickname.length > 10){
        result_display('nickname', '0', '昵称不能超过10个字符');
        window.nickname = false;
    }
    else{
        $.get('/account/nickname_judge/?nickname=' + nickname, function(result){
            json_result = eval('(' + result + ')');
            if (json_result.state == '1'){
                result_display('nickname', '1', '');
                window.nickname = true;
            }
            else if (json_result.state == '2'){
                result_display('nickname', '0', '当前昵称已存在');
                window.nickname = false;
            }
        });
    }
}

function password_judge(password){
	if (password == ''){
        result_display('password', '0', '密码不能为空');
        window.password = false;
    }
    else if (password.length < 6){
    	result_display('password', '0', '密码必须多于6位');
        window.password = false;
    }
    else if (password.length > 20){
        result_display('password', '0', '密码不能多于20位');
        window.password = false;
    }
    else{
    	result_display('password', '1', '');
        window.password = true;
    }
}

function password2_judge(password, password2){
    if (password2 == ''){
        result_display('password2', '0', '密码确认不能为空');
        window.password2 = false;
    }
    else if (password != password2){
        result_display('password2', '0', '两次密码不一致');
        window.password2 = false;
    }
    else{
        result_display('password2', '1', '');
        window.password2 = true;
    }
}

function email_judge(email){
	email_expr = /^(\w)+(\.\w+)*@(\w)+((\.\w+)+)$/;
    if (email == ''){
        result_display('email', '0', 'email地址不能为空');
        window.email = false;
    }
    else if (!email_expr.exec(email)){
    	result_display('email', '0', '请填写正确的email地址');
        window.email = false;
    }
    else{
        result_display('email', '1', '');
        window.email = true;
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
