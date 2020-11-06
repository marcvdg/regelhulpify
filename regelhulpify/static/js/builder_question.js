function deleteQuestionHandler(type) {
    let pathArray = window.location.pathname.split('/');
    const id = pathArray[3];
    pathArray.splice(-2, 2);
    const returnPath = pathArray.join('/')
    deleteItem(type, id, redirectHandler, returnPath)
    
}

document.addEventListener('DOMContentLoaded', (event) => {
    el =  document.querySelector('#question_delete');
    if (el) {
        el.addEventListener('click', () => { deleteQuestionHandler('question')});
    } else {
    document.querySelector('#result_delete').addEventListener('click', () => { deleteQuestionHandler('result')});
    }
});