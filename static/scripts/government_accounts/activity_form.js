$(document).ready(function () {
    jalaliDatepicker.startWatch({ time: false });
    $('#id_activity_date').on('input', function (e) { 
        e.preventDefault();
        var date_value = $('#id_activity_date').val();
        $('#id_activity_date').val(date_value.replaceAll('/', '-'));
    });
    $('#id_activity_result').change(function (e) { 
    e.preventDefault();
    if($('#id_activity_result').val() == 'do'){
            $("#id_activity_descriptions").removeAttr("disabled");
    }else{
            $("#id_activity_descriptions").attr("disabled","disabled");
    }
});
});