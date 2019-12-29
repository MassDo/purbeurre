$(document).ready(function() {

    function AutoCompleteSelectHandler(event, ui)
    {
    var selectedObj = ui.item;
    }
    // refactoring ==> make a loop
    // navbar form
    $(function() {
        $("#id_user_input").autocomplete({
            source: "/auto/",
            select: function (event, ui) { //item selected
            AutoCompleteSelectHandler(event, ui)
            },
            minLength: 2,
        });
    });
    // home page form
    $(function() {
        $("#id_main_form").autocomplete({
            source: "/auto/",
            select: function (event, ui) { //item selected
            AutoCompleteSelectHandler(event, ui)
            },
            minLength: 2,
        });
    });

    // addapt the width of autocomplete to the input field
    $.extend($.ui.autocomplete.prototype.options, {
        open: function(event, ui) {
            $(this).autocomplete("widget").css({
                "width": ($(this).width() + "px")
            });
        }
    });

});
