document.addEventListener('DOMContentLoaded', () => {
    
    $(".toast").toast({ delay:2000 });
    $(".toast").toast('show');
})

function showSnackbar() {
    // Get the snackbar DIV
    const sb = document.querySelector("#snackbar");
    sb.classList.add("show");

    // After 3 seconds, remove the show class from DIV
     setTimeout(()=>{ sb.classList.remove("show"); }, 5000);   
}

function deleteItem(type, id, nextAction, arg = ''){
    console.log(nextAction.this)
    
    let elementText = '';
    let url = '';
    switch (type) {
        case 'tool':
            elementText = 'tool';
            url = '/api/tool_delete/' + id + '/'
            break;
        case 'question':
            elementText = 'question';
            url = '/api/question_delete/' + id + '/'
            break;
        case 'result':
            elementText = 'result';
            url = '/api/question_delete/' + id + '/'
            break;    
        case 'answer':
            elementText = 'answer';
            url = '/api/answer_delete/' + id + '/'
            break;

    }
    const csrftoken = getCookie('csrftoken');
    const request = new Request(
        url,
        {headers: {'X-CSRFToken': csrftoken}}
    ); 
    if (confirm(`Are you sure that this ${elementText} doesn't spark joy?`)) {
        fetch(request, {
            method: 'DELETE',
            mode: 'same-origin',
            })
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