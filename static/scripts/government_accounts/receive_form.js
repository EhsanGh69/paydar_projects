$(document).ready(function () {
    jalaliDatepicker.startWatch({ time: true });
    $('#id_receive_date').on('input', function (e) { 
        e.preventDefault();
        var date_value = $('#id_receive_date').val();
        $('#id_receive_date').val(date_value.replaceAll('/', '-'));
    });
});