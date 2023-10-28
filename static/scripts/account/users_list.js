$(document).ready(function() {
    $("#search-btn").click(function() {
        if($('#search-input').val() != '' || $('#group-search').val() != ''){
            $("#search-form").submit();
       }
    });
});