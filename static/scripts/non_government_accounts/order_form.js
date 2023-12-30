$(document).ready(function () {
    jalaliDatepicker.startWatch({ time: false });
    $("#id_sended_image").attr("disabled","disabled");
    $("#id_sending_date").attr("disabled","disabled");
    $("#id_sended_image_type").attr("disabled","disabled");
    $("#id_explan_order_cancel").attr("disabled","disabled");
    $('#id_order_date').on('input', function (e) { 
        e.preventDefault();
        var date_value = $('#id_order_date').val();
        $('#id_order_date').val(date_value.replaceAll('/', '-'));
    });
    $('#id_sending_date').on('input', function (e) { 
        e.preventDefault();
        var date_value = $('#id_sending_date').val();
        $('#id_sending_date').val(date_value.replaceAll('/', '-'));
    });
    $('#id_order_result').change(function (e) { 
        e.preventDefault();
        if($('#id_order_result').val() == 'spd'){
            $("#id_sending_date").removeAttr("disabled");
        }else{
            $("#id_sending_date").attr("disabled","disabled");
        }
        if($('#id_order_result').val() == 'snd'){
            $("#id_sended_image").removeAttr("disabled");
            $("#id_sended_image_type").removeAttr("disabled");
        }else{
            $("#id_sended_image").attr("disabled","disabled");
            $("#id_sended_image_type").attr("disabled","disabled");
        }
        if($('#id_order_result').val() == 'cld'){
            $("#id_explan_order_cancel").removeAttr("disabled");
        }else{
            $("#id_explan_order_cancel").attr("disabled","disabled");
        }
    });
    if($('#id_order_result').val() == 'spd'){
        $("#id_sending_date").removeAttr("disabled");
    }else{
        $("#id_sending_date").attr("disabled","disabled");
    }
    if($('#id_order_result').val() == 'snd'){
        $("#id_sended_image").removeAttr("disabled");
        $("#id_sended_image_type").removeAttr("disabled");
    }else{
        $("#id_sended_image").attr("disabled","disabled");
        $("#id_sended_image_type").attr("disabled","disabled");
    }
    if($('#id_order_result').val() == 'cld'){
        $("#id_explan_order_cancel").removeAttr("disabled");
    }else{
        $("#id_explan_order_cancel").attr("disabled","disabled");
    }
    $('#id_unit_price').on('input', function(e) {
        e.preventDefault();
        var amount_value = $('#id_unit_price').val();
        $('#id_unit_price').val(String(amount_value).replace('-', ''))
        const numFormat = new Intl.NumberFormat();
        $('#counter').text(numFormat.format(amount_value));
    });
});