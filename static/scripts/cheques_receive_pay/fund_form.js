$(document).ready(function () {
    jalaliDatepicker.startWatch({ time: false });
    $("#submit-btn").attr("disabled", "disabled");
    if ($('#id_operation_type').val() == 'rem') {
        $("#rem-field").removeClass("d-none");
        $("#set-field").addClass("d-none");
        $("#submit-btn").removeAttr("disabled");
    } else if ($('#id_operation_type').val() == 'set') {
        $("#set-field").removeClass("d-none");
        $("#rem-field").addClass("d-none");
        $("#submit-btn").removeAttr("disabled");
    } else {
        $("#rem-field").addClass("d-none");
        $("#set-field").addClass("d-none");
        $("#submit-btn").attr("disabled", "disabled");
    }
    $('#id_operation_type').change(function (e) {
        e.preventDefault();
        if ($('#id_operation_type').val() == 'rem') {
            $("#rem-field").removeClass("d-none");
            $("#set-field").addClass("d-none");
            $("#submit-btn").removeAttr("disabled");
        } else if ($('#id_operation_type').val() == 'set') {
            $("#set-field").removeClass("d-none");
            $("#rem-field").addClass("d-none");
            $("#submit-btn").removeAttr("disabled");
        } else {
            $("#rem-field").addClass("d-none");
            $("#set-field").addClass("d-none");
            $("#submit-btn").attr("disabled", "disabled");
        }
    });
    $('#receipt_image-clear_id').change(function (e) {
        e.preventDefault();
        if (this.checked) {
            $("#receipt_image_alert").removeClass("d-none");
            $("#submit-btn").attr("type", "button");
        } else {
            $("#receipt_image_alert").addClass("d-none");
            $("#submit-btn").attr("type", "submit");
        }
    });
    $('#id_receipt_image').change(function (e) {
        e.preventDefault();
        $("#receipt_image_alert").addClass("d-none");
        $("#submit-btn").attr("type", "submit");
        $("#receipt_image-clear_id").prop("checked", false);
    });
    $('#charge_image-clear_id').change(function (e) {
        e.preventDefault();
        if (this.checked) {
            $("#charge_image_alert").removeClass("d-none");
            $("#submit-btn").attr("type", "button");
        } else {
            $("#charge_image_alert").addClass("d-none");
            $("#submit-btn").attr("type", "submit");
        }
    });
    $('#id_charge_image').change(function (e) {
        e.preventDefault();
        $("#charge_image_alert").addClass("d-none");
        $("#submit-btn").attr("type", "submit");
        $("#charge_image-clear_id").prop("checked", false);
    });
    $('#id_charge_date').on('input', function (e) {
        e.preventDefault();
        var date_value = $('#id_charge_date').val();
        $('#id_charge_date').val(date_value.replaceAll('/', '-'));
    });
    $('#id_removal_date').on('input', function (e) {
        e.preventDefault();
        var date_value = $('#id_removal_date').val();
        $('#id_removal_date').val(date_value.replaceAll('/', '-'));
    });
    const numFormat = new Intl.NumberFormat();
    $('#id_cost_amount').on('input', function(e) {
        e.preventDefault();
        var amount_value = $('#id_cost_amount').val();
        $('#id_cost_amount').val(String(amount_value).replace('-', ''))
        $('#cost_counter').text(numFormat.format(amount_value));
    });
    $('#id_charge_amount').on('input', function(e) {
        e.preventDefault();
        var amount_value = $('#id_charge_amount').val();
        $('#id_charge_amount').val(String(amount_value).replace('-', ''))
        $('#charge_counter').text(numFormat.format(amount_value));
    });
});