$(document).ready(function() {
    $("#search-btn").click(function() {
        if($('#date-filter').val() != 'all' || $('#search-input').val() != '' || $('#stuff-state').val() != 'all'){
            $("#search-form").submit();
       }
    });
});