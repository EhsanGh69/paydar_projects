$(document).ready(function() {
    const numFormat = new Intl.NumberFormat();
    $('#id_water_branch').on('input', function(e) {
        e.preventDefault();
        var amount_value = $('#id_water_branch').val();
        $('#id_water_branch').val(String(amount_value).replace('-', ''))
        $('#water_counter').text(numFormat.format(amount_value));
    });
    $('#id_electricity_branch').on('input', function(e) {
        e.preventDefault();
        var amount_value = $('#id_electricity_branch').val();
        $('#id_electricity_branch').val(String(amount_value).replace('-', ''))
        $('#electricity_counter').text(numFormat.format(amount_value));
    });
    $('#id_gas_branch').on('input', function(e) {
        e.preventDefault();
        var amount_value = $('#id_gas_branch').val();
        $('#id_gas_branch').val(String(amount_value).replace('-', ''))
        $('#gas_counter').text(numFormat.format(amount_value));
    });
    $('#id_phone_subscription').on('input', function(e) {
        e.preventDefault();
        var amount_value = $('#id_phone_subscription').val();
        $('#id_phone_subscription').val(String(amount_value).replace('-', ''))
        $('#phone_counter').text(numFormat.format(amount_value));
    });
    $('#id_designer_office').on('input', function(e) {
        e.preventDefault();
        var amount_value = $('#id_designer_office').val();
        $('#id_designer_office').val(String(amount_value).replace('-', ''))
        $('#designer_counter').text(numFormat.format(amount_value));
    });
    $('#id_supervisors').on('input', function(e) {
        e.preventDefault();
        var amount_value = $('#id_supervisors').val();
        $('#id_supervisors').val(String(amount_value).replace('-', ''))
        $('#supervisors_counter').text(numFormat.format(amount_value));
    });
    $('#id_engineer_system').on('input', function(e) {
        e.preventDefault();
        var amount_value = $('#id_engineer_system').val();
        $('#id_engineer_system').val(String(amount_value).replace('-', ''))
        $('#engineer_counter').text(numFormat.format(amount_value));
    });
    $('#id_sketch_map').on('input', function(e) {
        e.preventDefault();
        var amount_value = $('#id_sketch_map').val();
        $('#id_sketch_map').val(String(amount_value).replace('-', ''))
        $('#sketch_counter').text(numFormat.format(amount_value));
    });
    $('#id_export_permit').on('input', function(e) {
        e.preventDefault();
        var amount_value = $('#id_export_permit').val();
        $('#id_export_permit').val(String(amount_value).replace('-', ''))
        $('#permit_counter').text(numFormat.format(amount_value));
    });
    $('#id_export_end_work').on('input', function(e) {
        e.preventDefault();
        var amount_value = $('#id_export_end_work').val();
        $('#id_export_end_work').val(String(amount_value).replace('-', ''))
        $('#work_counter').text(numFormat.format(amount_value));
    });
});