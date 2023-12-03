$(document).ready(function() {
    jalaliDatepicker.startWatch({ time: false });
    $('#id_export_import_date').on('input', function (e) { 
        e.preventDefault();
        var date_value = $('#id_export_import_date').val();
        $('#id_export_import_date').val(date_value.replaceAll('/', '-'));
    });
});