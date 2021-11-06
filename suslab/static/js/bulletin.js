document.addEventListener('DOMContentLoaded', function() {
    const list = document.querySelector('.list');

    list.addEventListener('click', (event) => {
        row = event.target.closest('.item-expanded-row');
        row.querySelector('.row-details').classList.toggle('row-open');
    });
});