$(document).ready(function() {
    $("#search-btn").click(function() {
        if($('#search-input').val() != '' || $('#conflict-type').val() != 'all'){
            $("#search-form").submit();
    }
    });
});