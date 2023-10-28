$(document).ready(function() {
    $("#search-btn").click(function() {
        if($('#search-input').val() != '' || $('#date-filter').val() != 'all' || $('#payment-order').val() != 'all' || $('#buyer-seller').val() != 'all'){
            $("#search-form").submit();
       }
    });
});