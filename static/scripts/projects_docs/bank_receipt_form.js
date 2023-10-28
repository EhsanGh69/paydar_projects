$(document).ready(function () {
    jalaliDatepicker.startWatch({ time: false });
    $('#id_receipt_date').on('input', function (e) { 
        e.preventDefault();
        var date_value = $('#id_receipt_date').val();
        $('#id_receipt_date').val(date_value.replaceAll('/', '-'));
    });
});