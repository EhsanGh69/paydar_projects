$(document).ready(function () {
    $('#print-btn').click(function (e) { 
        e.preventDefault();

        $('.action-th').remove();
        $('.action-td').remove();
        $('.col-img').remove();
        $('.col-td').attr("colspan", "2");

        $('#data-table').printThis();

        setTimeout(function(){
            location.reload();
        }, 1000);
        
    });
    
});





