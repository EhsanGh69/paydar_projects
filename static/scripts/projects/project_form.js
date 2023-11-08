$(document).ready(function () {
    $("#id_contractual_salary").attr("disabled","disabled");
    $("#id_contractual_percentage").attr("disabled","disabled");
    $('#id_contract_type').change(function (e) { 
        e.preventDefault();
        if($('#id_contract_type').val() == 'co'){
            $("#id_contractual_salary").removeAttr("disabled");
            $("#id_contractual_percentage").removeAttr("disabled");
        }else{
            $("#id_contractual_salary").attr("disabled","disabled");
            $("#id_contractual_percentage").attr("disabled","disabled");
        }
    });
    $('#id_contractual_salary').on('input', function(e) {
        e.preventDefault();
        var amount_value = $('#id_contractual_salary').val();
        $('#id_contractual_salary').val(String(amount_value).replace('-', ''))
        const numFormat = new Intl.NumberFormat();
        $('#counter').text(numFormat.format(amount_value));
    });
});