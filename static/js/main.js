
var seed = -1;
$(".dog-refresh").click(function() {
    refresh()
})

function refresh(params) {
    $.ajax({
        type:"GET",
        url:"/getMarket",
        success: function(data) {
            $(".dogs").html(data['html']);
            if($(".dog-detail").length > 0){
                $("input[name='captcha-input']").first().focus();
                get_captcha()
            }
        }
    })
}

function get_captcha() {
    $.ajax({
        type:"GET",
        url:"/getCaptcha",
        success: function(data) {
            if(data['code']==200){
                $(".captcha-img").first().append(
                    "<img style='width: 200px;height:70px;' src='data:image/jpeg;base64,"+ data['img'] +"'>"
                )
                seed = data['seed']
                bind_();         
            }
        }
    })
}

function bind_() {
    var bind_input = $(".captcha-input").first();
    bind_input.bind('input propertychage', function() {
        console.log(bind_input.val());
        if (bind_input.val().length==4){
            var id = $("input[name='id']").val();
            console.log(id);
            var captcha = $(".captcha-input").val();
            purchase(id, captcha);
            bind_input = $(".captcha-input");
            if(bind_input.length < 1){
                refresh();
            }
            bind_input.first().focus();
        }
    })
}

function purchase(id, captcha) {
    var data = {
        "did":id,
        "seed":seed,
        "captcha":captcha
    }
    $.ajax({
        type:"GET",
        url:"/purchase",
        data:data,
        dataType:"json",
        success: function(data) {
            $(".msg").html("<span>" + data['msg'] + "</span>");
        }
    })

    $(".dog-detail").first().remove();
    get_captcha();
}

function check() {
    if($(".dog-detail").length == 0){
        window.location.reload();
    }
}

$(window).ready(function() {
    // focus
    refresh();
    setTimeout(check, 2000);
})
