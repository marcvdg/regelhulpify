document.addEventListener('DOMContentLoaded', () => {
    
    document.querySelector('#answer_add').addEventListener('click', () => { startWritingRows(1) });
    startWritingRows(3);
    document.querySelector('#answer_submit').addEventListener('click', () => { sendAnswers() });
    
})

async function startWritingRows(amount) {
    const question = getNumberFromUrl(3);
    let options = '<option value="">-------</option>'
    const nextListRaw = await fetch(`/api/answer_getnext/${question}/`);
    const nextList = await nextListRaw.json();
    nextList.forEach(item => {options += `<option value="${item.pk}">${item.text}</option>`})
    for (i = 0; i < amount; i++) { 
        writeAnswerFormRow(options)
    }
    return;
}

function getNumberFromUrl(x){
    let pathArray = window.location.pathname.split('/');
    return pathArray[x];
}

function writeAnswerFormRow(options) {
    const n =  document.getElementsByClassName("answer_row").length + 1;
    const focus = n == 1 ? 'autofocus' : ''
    const row = document.createElement('div');
    row.className = 'answer_row mt-3 mb-3 w-100 form-group';
    row.innerHTML = `
    <label for="id_text${n}">Answer ${n} text </label>
    <input type="text" name="text${n}" maxlength="128" class="form-control mb-2" required="" id="id_text${n}" ${focus}>
    <label for="id_nextquestion${n}">Next question or result</label><select name="nextquestion${n}" class="form-control" id="id_nextquestion${n}">
        ${options}
    `
    document.querySelector('#formzone').append(row)
}

function sendAnswers() {
    data = []
    const answerfields = document.querySelectorAll('.answer_row')
    answerfields.forEach((e) =>{
        d = {};
        d['text'] = e.querySelector('input').value;
        d['nextquestion'] = e.querySelector('select').value;
        if (d.text != "") {
            data.push(d)
        }
    })
    const question = getNumberFromUrl(3);
    const url = '/api/answers_add/' + question + '/' 
    const csrftoken = getCookie('csrftoken');
    const request = new Request(
        url,
        {headers: {'X-CSRFToken': csrftoken}}
        ); 
        
        fetch(request, {
            method: 'POST',
            mode: 'same-origin',
            body: JSON.stringify({
                data
            })
        })
        
    const tool = getNumberFromUrl(2);
    window.location.href = `/builder/${tool}/${question}/` 
}



