$(document).ready(function () {
    jalaliDatepicker.startWatch({ time: true });
    $('#id_export_receive_date').on('input', function (e) { 
        e.preventDefault();
        var date_value = $('#id_export_receive_date').val();
        $('#id_export_receive_date').val(date_value.replaceAll('/', '-'));
    });
    $('#id_due_date').on('input', function (e) { 
        e.preventDefault();
        var date_value = $('#id_due_date').val();
        $('#id_due_date').val(date_value.replaceAll('/', '-'));
    });  
});