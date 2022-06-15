let newCommentButton = document.querySelector('.new-comment-button');
let newAnswerButtons = document.querySelectorAll('.new-answer-button');
let cancelButtons = document.querySelectorAll('.cancel-button');


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

newCommentButton.addEventListener('click', createCommentDiv);

for (const button of newAnswerButtons) {
    button.addEventListener('click', createCommentDiv);
}

for (const button of cancelButtons) {
    button.addEventListener('click', removeCommentDiv);
}
