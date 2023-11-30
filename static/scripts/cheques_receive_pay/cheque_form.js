$(document).ready(function () {
    jalaliDatepicker.startWatch({ time: false });
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
    $('#id_cheque_amount').on('input', function(e) {
        e.preventDefault();
        var amount_value = $('#id_cheque_amount').val();
        $('#id_cheque_amount').val(String(amount_value).replace('-', ''))
        const numFormat = new Intl.NumberFormat();
        $('#counter').text(numFormat.format(amount_value));
    });
});