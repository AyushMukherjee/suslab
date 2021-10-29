document.addEventListener('DOMContentLoaded', function () {
    const navToggle = document.querySelector('.nav-toggle');
    const nav = document.querySelector('nav');
    
    const toggleNav = () => {
        nav.classList.toggle('nav-open');
        document.querySelector('.window-top>header').classList.toggle('hide');
        document.querySelector('.next-section').classList.toggle('hide');
    };

    navToggle.addEventListener('click', e => {
        e.stopPropagation();
        toggleNav();
    });

    nav.addEventListener('click', e => {
        e.stopPropagation();
    });

    document.querySelector('body').addEventListener('click', () => {
        if(nav.classList.contains('nav-open')) {
            toggleNav();
        }
     });
});
