var array = [
];
$(function () {
    var scrollTop = $(window) .scrollTop();
    $('#header') .addClass('fixed');
    $('#header-top, #header-top video, #header-top .flexslider, #header-top .flexslider li') .css({
        height: $(window) .height()
    });
    var isiPad = navigator.userAgent.match(/iPad/i) != null;
});
function scrolTo(el) {
    $('html, body') .animate({
        scrollTop: $('#' + el) .offset() .top - 50
    }, 500, function () {
        // $( '#disclaimer' ).remove();
    });
}
function Viewport() {
    fViewport();
    $(window) .bind('scroll', function (event) {
        fViewport();
    });
    // end scroll
    $(window) .resize(function () {
        fViewport();
    });
    function fViewport() {
        $('section:in-viewport') .each(function () {
            $(this) .addClass('animate');
        });
    }
    // end function fViewport()

}
// end function openViewoirt()

function next_boton() {
    $('.inner-redes a') .click(function (event) {
        if ($(this) .hasClass('checked')) {
            $(this) .removeClass('checked');
        } else {
            $(this) .addClass('checked');
        }
        if ($('#slide-4 .inner-redes .checked') .length)
        $('#slide-4 ') .find('.next') .show();
         else
        $('#slide-4 ') .find('.next') .hide();
        if ($('#slide-5 .inner-redes .checked') .length)
        $('#slide-5 ') .find('.next') .show();
         else
        $('#slide-5 ') .find('.next') .hide();
        if ($('#slide-6 .inner-redes .checked') .length)
        $('#slide-6 ') .find('.next') .show();
         else
        $('#slide-6 ') .find('.next') .hide();
        if ($('#slide-7 .inner-redes .checked') .length)
        $('#slide-7 ') .find('.next') .show();
         else
        $('#slide-7 ') .find('.next') .hide();
        if ($('#slide-8 .inner-redes .checked') .length)
        $('#slide-8 ') .find('.done') .show();
         else
        $('#slide-8 ') .find('.done') .hide();
        if ($('.gmail.checked') .length) {
            $('#slide-4 .cont-redes') .hide();
            $('#slide-4 #form-input, #slide-4 .next') .show();
        }
    });
}
