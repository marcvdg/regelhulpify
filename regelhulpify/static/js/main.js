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
    const csrftoken = getCookie('csrftoken');
    const request = new Request(
        url,
        {headers: {'X-CSRFToken': csrftoken}}
    ); 
    if (confirm(`Weet je zeker dat ${elementText} geen joy sparkt?`)) {
        fetch(request, {
            method: 'DELETE',
            mode: 'same-origin',
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

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}