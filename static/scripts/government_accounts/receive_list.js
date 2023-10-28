$(document).ready(function() {
    $("#search-btn").click(function() {
        if($('#search-input').val() != '' || $('#date-filter').val() != 'all'){
            $("#search-form").submit();
    }
    });
});