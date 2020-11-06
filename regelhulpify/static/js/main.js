document.addEventListener('DOMContentLoaded', () => {

    console.log("joe")  

})

function deleteItem(type, id, nextAction, arg = ''){
    console.log(nextAction.this)
    let elementText = '';
    let url = '';
    switch (type) {
        case 'tool':
            elementText = 'deze tool';
            url = '/api/tool_delete/' + id + '/'
            break;
        case 'question':
            elementText = 'deze vraag';
            url = '/api/question_delete/' + id + '/'
            break;
        case 'result':
            elementText = 'deze uitkomst';
            url = '/api/question_delete/' + id + '/'
            break;    
        case 'answer':
            elementText = 'dit antwoord';
            url = '/api/answer_delete/' + id + '/'
            break;

    }
    if (confirm(`Weet je zeker dat ${elementText} geen joy sparkt?`)) {
        fetch(url, {
            method: 'DELETE',
            })
        .then(() => console.log('whuuut'))
        .then(() => nextAction(arg))
        } else {
            console.log('Dan niet.');
    }
    
}

function redirectHandler(path) {
    window.location.assign(path);
}