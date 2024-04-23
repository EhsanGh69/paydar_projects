$(document).ready(function () {
    $('#id_investment_amount').on('input', function(e) {
        e.preventDefault();
        var amount_value = $('#id_investment_amount').val();
        $('#id_investment_amount').val(String(amount_value).replace('-', ''))
        const numFormat = new Intl.NumberFormat();
        $('#counter').text(numFormat.format(amount_value));
    });
});