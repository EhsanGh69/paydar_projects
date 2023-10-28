$(document).ready(function() {
    $("#search-btn").click(function() {
        if($('#operation-type').val() != 'all'){
            $("#search-form").submit();
       }
    });
});