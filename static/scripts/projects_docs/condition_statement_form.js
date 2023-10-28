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
});