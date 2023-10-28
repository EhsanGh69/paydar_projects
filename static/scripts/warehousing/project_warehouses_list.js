$(document).ready(function() {
    $("#search-btn").click(function() {
        if($('#search-input').val() != '' || $('#stuff-state').val() != 'all'){
            $("#search-form").submit();
       }
    });
});