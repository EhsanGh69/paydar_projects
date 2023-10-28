$(document).ready(function () {
    jalaliDatepicker.startWatch({ time: true });
    $('#id_payment_date').on('input', function (e) { 
        e.preventDefault();
        var date_value = $('#id_payment_date').val();
        $('#id_payment_date').val(date_value.replaceAll('/', '-'));
    });
    $('#id_payment_order').change(function (e) { 
        e.preventDefault();
        if($('#id_payment_order').val() == 'afc'){
            $("#id_current_roof").removeAttr("disabled");
        }else{
            $("#id_current_roof").attr("disabled","disabled");
        }
    });
});