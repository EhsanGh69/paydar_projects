$(document).ready(function() {
    $("#search-btn").click(function() {
        if($('#search-input').val() != '' || $('#date-filter').val() != 'all' || $('#is-returned').val() != 'all'){
            $("#search-form").submit();
       }
    });
});