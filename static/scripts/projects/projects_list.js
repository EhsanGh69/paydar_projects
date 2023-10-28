$(document).ready(function() {
    $("#search-btn").click(function() {
        if($('#search-input').val() != '' || $('#contract-type').val() != 'all'){
            $("#search-form").submit();
       }
    });
});