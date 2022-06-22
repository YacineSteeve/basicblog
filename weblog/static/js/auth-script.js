const input = document.querySelector('input');
const checkBox = document.querySelector('#id_blogger_creation_accepted');
const bloggerForm = document.querySelector('.blogger-form');
const avatarFile = document.querySelector('#id_avatar');
const errorsSection = document.querySelector('.form-errors');
const signUpButton = document.querySelector('#sign-up-btn');

input.focus();

function showForm() {
    bloggerForm.style.height = 'auto';
    bloggerForm.style.visibility = 'visible';
}

function hideForm() {
    bloggerForm.style.height = '0';
    bloggerForm.style.visibility = 'hidden';
    avatarFile.value = '';
}

function clearErrors() {
    while (errorsSection.firstChild) {
        errorsSection.removeChild(errorsSection.firstChild);
    }
}

checkBox.addEventListener('click', () => {
    checkBox.checked
        ? showForm()
        : hideForm();
})

if (errorsSection.firstChild) {
    signUpButton.addEventListener('click', clearErrors)
} else {
    signUpButton.removeEventListener('click', clearErrors)
}
