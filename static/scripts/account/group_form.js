$(document).ready(function () {
    $("#delete-btn").attr("disabled", "disabled");
    $("#id_permissions option").each(function(){
        if($(this).is(':selected')){
            $('#selected_permissions').append($('<option>', {
                value: $(this).val(),
                text: $(this).text()
           }));
        }
    });
    $('#id_permissions').change(function (e) { 
       e.preventDefault();

       $('#selected_permissions').children().remove();

       $("#id_permissions option").each(function(){
            if($(this).is(':selected')){
                $('#selected_permissions').append($('<option>', {
                    value: $(this).val(),
                    text: $(this).text()
               }));
            }
        });
   });

});