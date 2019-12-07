$(document).ready(function() {

    // Refactoring => make a loop
    $(function() {
        $("#id_user_input").autocomplete({
            source: "/auto/",
            select: function (event, ui) { //item selected
            AutoCompleteSelectHandler(event, ui)
            },
            minLength: 2,
        });
    });

    function AutoCompleteSelectHandler(event, ui)
    {
    var selectedObj = ui.item;
    }
    $(function() {
        $("#id_main_form").autocomplete({
            source: "/auto/",
            select: function (event, ui) { //item selected
            AutoCompleteSelectHandler(event, ui)
            },
            minLength: 2,
        });
    });

    function AutoCompleteSelectHandler(event, ui)
    {
    var selectedObj = ui.item;
    }

});
