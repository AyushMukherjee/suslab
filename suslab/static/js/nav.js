document.addEventListener('DOMContentLoaded', function () {
    const navToggle = document.querySelector('.nav-toggle');

    navToggle.addEventListener('click', () => {
    document.querySelector('nav').classList.toggle('nav-open');
    });
});