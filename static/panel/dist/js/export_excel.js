function ExportToExcel(type, fn, dl) {
    $('.action-th').remove();
    $('.action-td').remove();

    setTimeout(function(){
        location.reload();
    }, 1000);

    var elt = document.getElementById('data-table');
    var wb = XLSX.utils.table_to_book(elt, { sheet: "sheet1" });
    const now = new Date();
    return dl ?
        XLSX.write(wb, { bookType: type, bookSST: true, type: 'base64' }):
        XLSX.writeFile(wb, fn || ('receives'+ String(now.getTime()) + (type || '.xls')));
}