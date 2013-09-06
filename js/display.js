function vote(item_id, action){
	$.get('/main/vote_action/?item_id=' + item_id + '&action=' + action, function(result){
        json_result = eval('(' + result + ')');
        if (json_result.state == '1'){
        	if (action == '0'){
        		$('#disagree_div_' + item_id).html(json_result.num);
        		new_alert('投票成功', '1');
        	}
            else if (action == '1'){
            	$('#agree_div_' + item_id).html(json_result.num);
            	new_alert('投票成功', '1');
            }
        }
        else if (json_result.state == '2'){
        	new_alert('请先登录再进行操作', '2');
        }
        else if (json_result.state == '3'){
        	new_alert('当前用户已进行过投票', '2');
        }
    });
}

function image_change(item_id){
	var image_src = $('#image_' + item_id).attr('src');
	var mode = image_src.split('?')[1]
	image_src = image_src.split('?')[0]
	if (mode == 'mode=1'){
		$('#image_' + item_id).attr('src', image_src);
	}
    else{
        img_scroll = $('#image_' + item_id).offset().top;
        $(window).scrollTop(img_scroll-150);
    	$('#image_' + item_id).attr('src', image_src + '?mode=1');
    }
}

function comment_show(item_id){
	if ($('#comment_show_' + item_id).is(':hidden')){
		$.get('/main/comment_show/?item_id=' + item_id, function(result){
			$('#comment_all_' + item_id).html(result);
        });
        $('#comment_show_' + item_id).show();
	}
    else{
    	$('#comment_show_' + item_id).hide();
    }
}

function comment_action(item_id){
	context = $('#context_' + item_id).val();
	if (context == ''){
		new_alert('评论内容不能为空', '2');
	}
	else if (context.length > 80){
		new_alert('评论内容不能超过80个字符', '2');
	}
	else{
		$.get('/main/comment_action/?item_id=' + item_id + '&context=' + context, function(result){
            $('#comment_add_' + item_id).html(result);
        });
	}
}
