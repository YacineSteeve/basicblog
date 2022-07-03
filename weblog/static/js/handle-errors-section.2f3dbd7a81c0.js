const errorsSections = document.querySelectorAll('.form-errors');
const submitButtons = document.querySelectorAll('input[type=submit]');


function clearErrors() {
    for (const section of errorsSections) {
        while (section.firstChild) {
            console.log('doing');
            section.removeChild(section.firstChild);
        }
    }
}

for (const section of errorsSections) {
    if (section.firstChild) {
        for (const button of submitButtons) {
            button.addEventListener('click', clearErrors);
        }
    } else {
        for (const button of submitButtons) {
            button.removeEventListener('click', clearErrors);
        }
    }
}
