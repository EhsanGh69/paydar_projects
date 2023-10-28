$(document).ready(function () {
    jalaliDatepicker.startWatch({ time: false });
    $("#id_letter_type").attr("disabled", "disabled");
    $("#id_license_type").attr("disabled", "disabled");
    $('#id_doc_type').change(function (e) {
        e.preventDefault();
        if ($('#id_doc_type').val() == 'let') {
            $("#letter-star").removeClass("d-none");
            $("#license-star").addClass("d-none");
            $("#id_letter_type").removeAttr("disabled");
            $("#id_license_type").attr("disabled", "disabled");
        } else if ($('#id_doc_type').val() == 'lic') {
            $("#license-star").removeClass("d-none");
            $("#letter-star").addClass("d-none");
            $("#id_license_type").removeAttr("disabled");
            $("#id_letter_type").attr("disabled", "disabled");
        } else {
            $("#letter-star").addClass("d-none");
            $("#license-star").addClass("d-none");
            $("#id_letter_type").attr("disabled", "disabled");
            $("#id_license_type").attr("disabled", "disabled");
        }
    });
    if ($('#id_doc_type').val() == 'let') {
        $("#letter-star").removeClass("d-none");
        $("#license-star").addClass("d-none");
        $("#id_letter_type").removeAttr("disabled");
        $("#id_license_type").attr("disabled", "disabled");
    } else if ($('#id_doc_type').val() == 'lic') {
        $("#license-star").removeClass("d-none");
        $("#letter-star").addClass("d-none");
        $("#id_license_type").removeAttr("disabled");
        $("#id_letter_type").attr("disabled", "disabled");
    } else {
        $("#letter-star").addClass("d-none");
        $("#license-star").addClass("d-none");
        $("#id_letter_type").attr("disabled", "disabled");
        $("#id_license_type").attr("disabled", "disabled");
    }
    $('#id_send_receive_date').on('input', function (e) { 
        e.preventDefault();
        var date_value = $('#id_send_receive_date').val();
        $('#id_send_receive_date').val(date_value.replaceAll('/', '-'));
    });
});