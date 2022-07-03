let newCommentButton = document.querySelector('.new-comment-button');
let newAnswerButtons = document.querySelectorAll('.new-answer-button');
let cancelButtons = document.querySelectorAll('.cancel-button');
let newCategoryButton = document.querySelector('.show-new-category-form');
let cancelNewCategoryButton = document.querySelector('#cancel-new-category-button');
let categoryForm = document.querySelector('.new-category-form');
let categoryNameInput = document.querySelector('#id_name');


function showCategoryForm() {
    categoryForm.style.height = 'fit-content';
    categoryForm.style.visibility = 'visible';
    categoryNameInput.focus();
    categoryForm.scrollIntoView({block: 'center', behavior: 'smooth'});
}


function hideCategoryForm() {
    categoryForm.style.visibility = 'hidden';
    categoryForm.style.height = '0';
}


function removeCommentDiv(event) {
    let commentDiv = event.target.parentNode.parentNode
    let commentButton = event.target.parentNode.parentNode.parentNode.childNodes[event.target.parentNode.parentNode.parentNode.childNodes.length - 4];
    console.log(commentButton);
    commentButton.style.height = 'fit-content';
    commentButton.style.visibility = 'visible';
    commentDiv.style.height = '0';
    commentDiv.style.marginTop = '0';
    commentDiv.style.visibility = 'hidden';
}


function createCommentDiv(event) {
    let commentDiv = event.target.parentNode.childNodes[event.target.parentNode.childNodes.length - 2];
    let commentButton = event.target;

    commentButton.style.height = '0';
    commentButton.style.visibility = 'hidden';
    commentDiv.style.height = '35vh';
    commentDiv.style.marginTop = '5vh';
    commentDiv.style.visibility = 'visible';

    commentDiv.scrollIntoView({block: 'center', behavior: 'smooth'});
}


newCategoryButton.addEventListener('click', showCategoryForm);

cancelNewCategoryButton.addEventListener('click', hideCategoryForm);

newCommentButton.addEventListener('click', createCommentDiv);

for (const button of newAnswerButtons) {
    button.addEventListener('click', createCommentDiv);
}

for (const button of cancelButtons) {
    button.addEventListener('click', removeCommentDiv);
}
