$(document).ready(function () {
    jalaliDatepicker.startWatch({ time: true });
    $('#id_follow_date').on('input', function (e) { 
        e.preventDefault();
        var date_value = $('#id_follow_date').val();
        $('#id_follow_date').val(date_value.replaceAll('/', '-'));
    });
});