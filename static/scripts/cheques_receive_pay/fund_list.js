$(document).ready(function() {
    $("#search-btn").click(function() {
        if($('#search-input').val() != '' || $('#date-filter').val() != 'all' || $('#operation-type').val() != 'all'){
            $("#search-form").submit();
       }
    });
});