$(document).ready(function () {
    jalaliDatepicker.startWatch({ time: false });
    $('#id_agreement_date').on('input', function (e) { 
        e.preventDefault();
        var date_value = $('#id_agreement_date').val();
        $('#id_agreement_date').val(date_value.replaceAll('/', '-'));
    });
});