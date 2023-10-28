$(document).ready(function () {
    jalaliDatepicker.startWatch({ time: true });
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
    $('#removal_image-clear_id').change(function (e) {
        e.preventDefault();
        if (this.checked) {
            $("#removal_image_alert").removeClass("d-none");
            $("#submit-btn").attr("type", "button");
        } else {
            $("#receipt_image_alert").addClass("d-none");
            $("#submit-btn").attr("type", "submit");
        }
    });
    $('#id_removal_image').change(function (e) {
        e.preventDefault();
        $("#removal_image_alert").addClass("d-none");
        $("#submit-btn").attr("type", "submit");
        $("#removal_image-clear_id").prop("checked", false);
    });
    $('#settle_image-clear_id').change(function (e) {
        e.preventDefault();
        if (this.checked) {
            $("#settle_image_alert").removeClass("d-none");
            $("#submit-btn").attr("type", "button");
        } else {
            $("#settle_image_alert").addClass("d-none");
            $("#submit-btn").attr("type", "submit");
        }
    });
    $('#id_settle_image').change(function (e) {
        e.preventDefault();
        $("#settle_image_alert").addClass("d-none");
        $("#submit-btn").attr("type", "submit");
        $("#settle_image-clear_id").prop("checked", false);
    });
});