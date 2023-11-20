$(document).ready(function () {
    jalaliDatepicker.startWatch({ time: false });
    $('#id_payment_date').on('input', function (e) { 
        e.preventDefault();
        var date_value = $('#id_payment_date').val();
        $('#id_payment_date').val(date_value.replaceAll('/', '-'));
    });
});