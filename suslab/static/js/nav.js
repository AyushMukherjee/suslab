document.addEventListener('DOMContentLoaded', function () {
    const navToggle = document.querySelector('.nav-toggle');

    navToggle.addEventListener('click', () => {
        document.querySelector('nav').classList.toggle('nav-open');
        document.querySelector('.window-top>header').classList.toggle('hide');
    });
});
