document.addEventListener('DOMContentLoaded', function() {
    const list = document.querySelector('.list');
    const searchIcons = document.querySelectorAll('.search-icon');

    document.querySelector('body').addEventListener('click', () => {
        document.querySelectorAll('.active,.row-open').forEach(
            el => el.classList.remove('active', 'row-open')
        );
     });

    searchIcons.forEach(icon => icon.addEventListener('click', (event) => {
        event.stopPropagation();
        sibling = icon.previousElementSibling;
        sibling.classList.toggle('active');
        sibling.focus();
    }));

    if(list.dataset.auth === "True"){
        list.addEventListener('click', (event) => {
            event.stopPropagation();
            row = event.target.closest('.item-expanded-row');
            rowDetails = row.querySelector('.row-details');
            expanded = document.querySelectorAll('.row-open').forEach(
                openRow =>  {
                    if(openRow !== rowDetails) openRow.classList.remove('row-open');
                }
            );
            rowDetails.classList.toggle('row-open');
        });
    };
});