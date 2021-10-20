document.addEventListener('DOMContentLoaded', function () {
  const togglePassword = document.querySelector('#togglePassword');
  const password = document.querySelector('#password');
  
  togglePassword.addEventListener('click', e => {
    type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);
    console.log(this);
    togglePassword.classList.toggle('fa-eye-slash');
  });
});