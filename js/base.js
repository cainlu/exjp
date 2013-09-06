$(document).ready(function(){
    $('.comment_form input').keydown(function(e){
        var keyCode = e.keyCode ? e.keyCode : e.which ? e.which : e.charCode;
        if (keyCode == 13){
            return false;
        }
    })
});

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
	cache: false,
    crossDomain: false,
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            var csrftoken = $.cookie('csrftoken');
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        }
    }
});

function new_alert(context, type){
	if (type == '1'){
        var x = noty({layout: 'center', text: context, type: 'success'});
    }
    else if (type == '2'){
        var x = noty({layout: 'center', text: context, type: 'warning'});
    }
}
