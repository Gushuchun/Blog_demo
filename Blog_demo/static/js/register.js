$(function() {
    $("get_captcha").click(function(event) {
        let $this = $(this);
        let email = $("input[name='email']").val();
        if(!email){
            alert("Please enter a valid email");
            return;
        }
        //取消按钮的的点击事件
        $this.off('click');
        //倒计时
        setInterval(function() {})
    })
})