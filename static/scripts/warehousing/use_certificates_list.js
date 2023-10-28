$(document).ready(function() {
    $("#search-btn").click(function() {
        if($('#search-input').val() != '' || $('#stuff-state').val() != 'all' || $('#return-to').val() != 'all'){
            $("#search-form").submit();
        }
    });
    if($('#stuff-state').val() != 'all'){
        $('#return-to').attr("disabled","disabled");
    }else {
        $('#return-to').removeAttr("disabled");;
    }
    if($('#return-to').val() != 'all'){
        $('#stuff-state').attr("disabled","disabled");
    }else {
        $('#stuff-state').removeAttr("disabled");;
    }
    $('#stuff-state').change(function (e) {
        if($(this).val() != 'all'){
            $('#return-to').attr("disabled","disabled");
        }else {
            $('#return-to').removeAttr("disabled");;
        }
    });
    $('#return-to').change(function (e) {
        if($(this).val() != 'all'){
        $('#stuff-state').attr("disabled","disabled");
        }else {
            $('#stuff-state').removeAttr("disabled");;
        }
    });
});