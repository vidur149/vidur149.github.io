$(function() {
    $(".inc-btn").click(increment);

    $(".bg-btn").click(changeBg);

    function increment() {
        $('.counter').html(parseInt($('.counter').html(), 10) + 1)
    }

    function changeBg() {
        $(".bg-div").toggleClass(function() {
            if ($(this).is(".red")) {
                return "blue";
            } else {
                return "red";
            }
        });
    }
});