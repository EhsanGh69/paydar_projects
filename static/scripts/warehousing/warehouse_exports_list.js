$(document).ready(function() {
    $("#search-btn").click(function() {
        if($('#search-input').val() != ''){
            $("#search-form").submit();
       }
    });
});