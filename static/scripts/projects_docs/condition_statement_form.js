$(document).ready(function () {
    $("#id_final_deposit_amount").attr("disabled", "disabled");
    $('#id_management_confirm').change(function (e) {
        e.preventDefault();
        if ($('#id_management_confirm').val() == 'con') {
            $("#id_final_deposit_amount").removeAttr("disabled");
        } else {
            $("#id_final_deposit_amount").attr("disabled", "disabled");
        }
    });
    if ($("#id_management_confirm").val() == 'con') {
        $("#id_final_deposit_amount").removeAttr("disabled");
    } else {
        $("#id_final_deposit_amount").attr("disabled", "disabled");
    }
    const numFormat = new Intl.NumberFormat();
    $('#id_requested_amount').on('input', function(e) {
        e.preventDefault();
        var amount_value = $('#id_requested_amount').val();
        $('#id_requested_amount').val(String(amount_value).replace('-', ''));
        $('#request_counter').text(numFormat.format(amount_value));
    });
    $('#id_confirmed_amount').on('input', function(e) {
        e.preventDefault();
        var amount_value = $('#id_confirmed_amount').val();
        $('#id_confirmed_amount').val(String(amount_value).replace('-', ''));
        $('#confirm_counter').text(numFormat.format(amount_value));
    });
    $('#id_final_deposit_amount').on('input', function(e) {
        e.preventDefault();
        var amount_value = $('#id_final_deposit_amount').val();
        $('#id_final_deposit_amount').val(String(amount_value).replace('-', ''));
        $('#final_counter').text(numFormat.format(amount_value));
    });
});