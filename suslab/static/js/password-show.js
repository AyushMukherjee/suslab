document.addEventListener('DOMContentLoaded', function () {
  const togglePasswordList = document.querySelectorAll('.toggle-password');
  
  togglePasswordList.forEach(button => button.addEventListener('click', () => {
    password = button.previousElementSibling;
    type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);
    button.classList.toggle('fa-eye-slash');
  }));
});
