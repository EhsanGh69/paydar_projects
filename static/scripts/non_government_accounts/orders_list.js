$(document).ready(function() {
    $("#search-btn").click(function() {
        if($('#search-input').val() != '' || $('#date-filter').val() != 'all' || $('#order-result').val() != 'all' || $('#order-image-type').val() != 'all'){
            $("#search-form").submit();
        }
    });
});