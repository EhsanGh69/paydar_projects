$(document).ready(function () {
    jalaliDatepicker.startWatch({ time: true });
    $('#id_date').on('input', function (e) { 
        e.preventDefault();
        var date_value = $('#id_date').val();
        $('#id_date').val(date_value.replaceAll('/', '-'));
    });
});