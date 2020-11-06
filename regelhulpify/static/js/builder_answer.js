function deleteAnswerHandler() {
    let pathArray = window.location.pathname.split('/');
    const id = pathArray[4];
    pathArray.splice(-2, 2);
    const returnPath = pathArray.join('/')
    deleteItem('answer', id, redirectHandler, returnPath)
    
}

document.addEventListener('DOMContentLoaded', (event) => {
    document.querySelector('#answer_delete').addEventListener('click', deleteAnswerHandler);
});