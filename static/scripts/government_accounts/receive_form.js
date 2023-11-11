$(document).ready(function () {
    jalaliDatepicker.startWatch({ time: false });
    $('#id_receive_date').on('input', function (e) { 
        e.preventDefault();
        var date_value = $('#id_receive_date').val();
        $('#id_receive_date').val(date_value.replaceAll('/', '-'));
    });
    $('#id_receive_amount').on('input', function(e) {
        e.preventDefault();
        var amount_value = $('#id_receive_amount').val();
        $('#id_receive_amount').val(String(amount_value).replace('-', ''))
        const numFormat = new Intl.NumberFormat();
        $('#counter').text(numFormat.format(amount_value));
    });
});