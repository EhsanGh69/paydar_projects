$(document).ready(function () {
    jalaliDatepicker.startWatch({ time: true });
    $('#id_date').on('input', function (e) { 
        e.preventDefault();
        var date_value = $('#id_date').val();
        $('#id_date').val(date_value.replaceAll('/', '-'));
    });
    $('#id_amount').on('input', function(e) {
        e.preventDefault();
        var amount_value = $('#id_amount').val();
        $('#id_amount').val(String(amount_value).replace('-', ''))
        const numFormat = new Intl.NumberFormat();
        $('#counter').text(numFormat.format(amount_value));
    });
});