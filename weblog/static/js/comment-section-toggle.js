let newCommentButton = document.querySelector('.new-comment-button');
let newAnswerButtons = document.querySelectorAll('.new-answer-button');


function removeCommentDiv(event) {
    let commentButton = document.createElement('button');

    commentButton.classList.add('comment-button');
    commentButton.setAttribute('type', 'button');
    commentButton.addEventListener('click', createCommentDiv);

    if (event.target.parentNode.parentNode.parentNode.className === 'blog-post-comments') {
        commentButton.classList.add('new-comment-button', 'element-to-center');
        commentButton.textContent = 'Add a comment';
    } else {
        commentButton.classList.add('new-answer-button');
        commentButton.textContent = 'Answer';
    }

    event.target.parentNode.parentNode.parentNode.appendChild(commentButton);
    event.target.parentNode.parentNode.parentNode.removeChild(event.target.parentNode.parentNode);
}

function createCommentDiv(event) {
    let commentDiv = document.createElement('div');
    let fakeLabel = document.createElement('label');
    let textArea = document.createElement('textarea');
    let newCommentButtonsDiv = document.createElement('div');
    let cancelButton = document.createElement('button');
    let postButton = document.createElement('button');

    commentDiv.classList.add('new-comment');

    fakeLabel.setAttribute('for', 'comment-text-area');
    textArea.setAttribute('cols', '25');
    textArea.setAttribute('rows', '5');
    textArea.setAttribute('wrap', 'soft');
    textArea.setAttribute('name', 'comment-text-area');
    textArea.setAttribute('placeholder', 'Enter your comment');
    textArea.setAttribute('autocomplete', 'on');
    textArea.setAttribute('spellcheck', 'true');
    textArea.setAttribute('minlength', '1');
    textArea.setAttribute('maxlength', '255');
    textArea.setAttribute('id', 'comment-text-area');

    newCommentButtonsDiv.classList.add('new-comment-buttons');

    cancelButton.setAttribute('type', 'button');
    cancelButton.classList.add('comment-button', 'cancel-button');
    cancelButton.textContent = 'Cancel';
    cancelButton.addEventListener('click', removeCommentDiv);

    postButton.setAttribute('type', 'button');
    postButton.classList.add('comment-button', 'post-button');
    postButton.textContent = 'Post'

    newCommentButtonsDiv.appendChild(cancelButton);
    newCommentButtonsDiv.appendChild(postButton);

    commentDiv.appendChild(fakeLabel);
    commentDiv.appendChild(textArea);
    commentDiv.appendChild(newCommentButtonsDiv);

    event.target.parentNode.appendChild(commentDiv);
    event.target.parentNode.removeChild(event.target);

    commentDiv.scrollIntoView({block: 'center', behavior: 'smooth'});
}

newCommentButton.addEventListener('click', createCommentDiv);

for (const button of newAnswerButtons) {
    button.addEventListener('click', createCommentDiv);
}
