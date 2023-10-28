$(document).ready(function() {
    $("#search-btn").click(function() {
        if($('#search-input').val() != '' || $('#date-filter').val() != 'all' || $('#proceeding-type').val() != 'all'){
            $("#search-form").submit();
       }
    });
});