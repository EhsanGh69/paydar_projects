$(document).ready(function () {
    jalaliDatepicker.startWatch({ time: false });
    $("#id_project_returned").attr("disabled","disabled");
    $('#id_import_date').on('input', function (e) { 
        e.preventDefault();
        var date_value = $('#id_import_date').val();
        $('#id_import_date').val(date_value.replaceAll('/', '-'));
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