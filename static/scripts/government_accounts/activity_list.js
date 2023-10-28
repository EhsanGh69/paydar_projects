$(document).ready(function() {
    $("#search-btn").click(function() {
        if($('#search-input').val() != '' || $('#date-filter').val() != 'all' || $('#activity-result').val() != 'all'){
            $("#search-form").submit();
        }
    });
});