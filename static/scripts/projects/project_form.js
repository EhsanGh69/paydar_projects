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
});