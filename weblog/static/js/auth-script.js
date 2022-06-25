const input = document.querySelector('input');
const checkBox = document.querySelector('#id_blogger_creation_accepted');
const bloggerForm = document.querySelector('.blogger-form');
const avatarFile = document.querySelector('#id_avatar');

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

checkBox.addEventListener('click', () => {
    checkBox.checked
        ? showForm()
        : hideForm();
})
