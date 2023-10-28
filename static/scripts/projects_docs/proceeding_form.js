$(document).ready(function () {
    jalaliDatepicker.startWatch({ time: false });
    $('#id_proceeding_date').on('input', function (e) { 
        e.preventDefault();
        var date_value = $('#id_proceeding_date').val();

        $('#id_proceeding_date').val(date_value.replaceAll('/', '-'));
    });
});