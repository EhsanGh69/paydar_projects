$(document).ready(function() {
    $("#search-btn").click(function() {
        if($('#date-filter').val() != 'all' || $('#search-input').val() != ''){
            $("#search-form").submit();
       }
    });
});