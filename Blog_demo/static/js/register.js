$(function () {
    function bindCaptchaClick() {
        $("#get_captcha").click(function (event) {
            let $this = $(this);
            let email = $("input[name='email']").val();
            if (!email) {
                alert("Please enter a valid email");
                return;
            }
            //取消按钮的的点击事件
            $this.off('click');
            //发送ajax请求
            $.ajax('/author/captcha?email=' + email, {
                method: 'GET',
                success: function (result) {
                    console.log(result);
                    if(result['code'] == 200) {
                        alert("Verification Code Sent Successfully!");
                    }else {
                        alert(result['message']);
                    }

                },
                error: function (error) {
                    alert("Please enter a valid email");
                    console.log(error);
                }
            })
            //倒计时
            let countdown = 6;
            let timer = setInterval(function () {
                if (countdown<=0) {
                    $this.text('Get VCode')
                    //清掉定时器
                    clearInterval(timer);
                    //重新绑定点击事件
                    bindCaptchaClick();
                } else {
                    countdown--;
                    $this.text(countdown + "s")
                }
            }, 1000);
        })
    }

    bindCaptchaClick();
})