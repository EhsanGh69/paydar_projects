$(document).ready(function () {
    jalaliDatepicker.startWatch({ time: false });
    $("#id_deficient_amount").attr("disabled","disabled");
    $("#id_excess_amount").attr("disabled","disabled");
    $("#id_returned_to").attr("disabled","disabled");
    $("#id_return_date").attr("disabled","disabled");
    $('#id_is_deficient').change(function (e) { 
        e.preventDefault();
        if(this.checked){
            $("#deficient_alert").removeClass("d-none");
            $("#id_deficient_amount").removeAttr("disabled");
            $("#id_is_excess").attr("disabled","disabled");
            $("#submit-btn").attr("type","button");
        }else{
            $("#deficient_alert").addClass("d-none");
            $("#id_deficient_amount").attr("disabled","disabled");
            $("#submit-btn").attr("type","submit");
            $("#id_is_excess").removeAttr("disabled");
        }
    });
    $('#id_deficient_amount').change(function (e) { 
        e.preventDefault();
        $("#deficient_alert").addClass("d-none");
        $("#submit-btn").attr("type","submit");
    });
    $('#id_is_excess').change(function (e) { 
        e.preventDefault();
        if(this.checked){
            $("#id_is_deficient").attr("disabled","disabled");
            $("#excess_alert").removeClass("d-none");
            $("#return_alert").removeClass("d-none");
            $("#id_excess_amount").removeAttr("disabled");
            $("#id_returned_to").removeAttr("disabled");
            $("#id_return_date").removeAttr("disabled");
            $("#submit-btn").attr("type","button");
        }else{
            $("#id_is_deficient").removeAttr("disabled");
            $("#excess_alert").addClass("d-none");
            $("#return_alert").addClass("d-none");
            $("#id_excess_amount").attr("disabled","disabled");
            $("#id_returned_to").attr("disabled","disabled");
            $("#id_return_date").attr("disabled","disabled");
            $("#submit-btn").attr("type","submit");
        }
    });
    $('#id_excess_amount,#id_returned_to,#id_return_date').change(function (e) { 
        e.preventDefault();
        $("#excess_alert").addClass("d-none");
        $("#return_alert").addClass("d-none");
        $("#submit-btn").attr("type","submit");
    });
    $('#id_start_using_date').on('input', function (e) { 
        e.preventDefault();
        var date_value = $('#id_start_using_date').val();

        $('#id_start_using_date').val(date_value.replaceAll('/', '-'));
    });
    $('#id_finish_using_date').on('input', function (e) { 
        e.preventDefault();
        var date_value = $('#id_finish_using_date').val();

        $('#id_finish_using_date').val(date_value.replaceAll('/', '-'));
    });
    $('#id_return_date').on('input', function (e) { 
        e.preventDefault();
        var date_value = $('#id_return_date').val();

        $('#id_return_date').val(date_value.replaceAll('/', '-'));
    });
});