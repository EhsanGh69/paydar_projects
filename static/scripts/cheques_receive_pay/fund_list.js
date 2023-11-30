$(document).ready(function() {
    $("#search-btn").click(function() {
        if($('#search-input').val() != '' || $('#operation-type').val() != 'all'){
            $("#search-form").submit();
       }
    });
});