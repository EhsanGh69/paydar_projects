$(document).ready(function () {
    $('#print-btn').click(function (e) { 
        e.preventDefault();

        $('.action-th').remove();
        $('.action-td').remove();

        $('#data-table').printThis();

        setTimeout(function(){
            location.reload();
        }, 1000);
        
    });
    
});





