document.addEventListener('DOMContentLoaded', () => {

})

function showSnackbar() {
    // Get the snackbar DIV
    const sb = document.querySelector("#snackbar");
    sb.classList.add("show");

    // After 3 seconds, remove the show class from DIV
     setTimeout(()=>{ sb.classList.remove("show"); }, 5000);   
}

function createToolsBtn(element){
    // Create post
    const tool = document.createElement('div');
        tool.className = 'tool_link rounded my-3 p-3 bg-light';
        tool.id = element.id
        tool.innerHTML = `<a href="/${element.pk}" class="btn btn-primary mt-2 mb-2">
            ${element.fields.name}
            </a>
            <div class="">${element.fields.desc}</div>`
        if (element.fields.img != null){
            tool.style.background = `linear-gradient(to right, rgba(248,249,250,1) 30%,
                rgba(248,249,250,0)), url(${element.fields.img})`;
            tool.style.backgroundSize = 'cover';
        }
        document.querySelector('#tools_list').append(tool)
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