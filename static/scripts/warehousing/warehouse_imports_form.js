$(document).ready(function () {
    jalaliDatepicker.startWatch({ time: true });
    $("#id_project_returned").attr("disabled","disabled");
    $('#id_date_time').on('input', function (e) { 
        e.preventDefault();
        var date_value = $('#id_date_time').val();
        $('#id_date_time').val(date_value.replaceAll('/', '-'));
    });
    $('#id_is_returned').change(function (e) { 
        e.preventDefault();
        if(this.checked){
            $("#id_project_returned").removeAttr("disabled");
        }else{
            $("#id_project_returned").attr("disabled","disabled");
        }
    });
});