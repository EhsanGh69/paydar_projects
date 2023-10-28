$(document).ready(function() {
    $("#search-btn").click(function() {
        if($('#search-input').val() != '' || $('#doc-type').val() != 'all'){
            $("#search-form").submit();
       }
    });
});