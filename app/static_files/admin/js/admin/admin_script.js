document.addEventListener('DOMContentLoaded', function () {
    var rows = document.querySelectorAll('.field-proximo');
    console.log("cosas");
    rows.forEach(function (row) {
        var value = row.textContent.trim();
        console.log(value);
        if (value === 'Today is a great day' || value === '7' || value === '6' || value === '5' || value === '4') {
            row.parentElement.style.boxShadow = 'inset 1pt 1pt 11pt 1pt green';
        } else if ( value === '1' || value === '2' || value === '3') {
            row.parentElement.style.boxShadow = 'inset 1pt 1pt 11pt 1pt orange';
        } else if (value === 'Estamos atrasados') {
            row.parentElement.style.boxShadow = 'inset 1pt 1pt 11pt 1pt red';
            
        }
    });
});
