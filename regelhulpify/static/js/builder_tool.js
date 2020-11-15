document.addEventListener('DOMContentLoaded', (event) => {
    document.querySelector("#tool_delete").addEventListener('click', deleteToolHandler)
    getTool();
});

function deleteToolHandler() {
    const path = window.location.pathname.split('/');
    const id = path[2]
    const returnPath = '/builder'
    deleteItem('tool', id, redirectHandler, returnPath)
}

function deleteQuestionHandler(id){
    deleteItem('question', id, getTool)
    
}

// Swaps question position attribute with the one above or below, if possible
function moveQuestion(id, direction){
    const url = '/api/question_move/' + id + '/' + direction + '/'
    console.log(url); 
    fetch(url, {
        method: 'PUT',
        })
        .then(() => getTool())
}

function writeQuestion(element){
    // Write line
    const question = document.createElement('div');
    question.className = 'question-name rh-box rounded bg-light p-2 my-3';
    let r_label = element.result ? '<div class="text-muted small">Uitkomst </div>' : '';
    question.id = `q_${element.pk}`
    let answer_html = ''
    // Create answer lines
    if (!(element.result)){
        element.answers.forEach(a => {
            answer_html += `<li><a href="/builder/${element.tool}/${element.id}/${a.id}"><span class="text-muted">${a.text.replace(/"|'/g, '&apos;')} &rarr; ${a.nexttext.replace(/"|'/g, '&apos;')}</span></a></li>`
        });
        answer_html += `<li><a class="text-muted" href="/builder/${element.tool}/${element.id}/newanswer">Nieuw antwoord...</a></li>`;
    }
    question.innerHTML = `${r_label}<a href="/builder/${element.tool}/${element.id}" class="mt-4 pr-5">${element.text.replace(/"|'/g, '&apos;')}</a>
                        
                        <div class="">${element.expl.replace(/"|'/g, '&apos;')}</div>
                        <ul>${answer_html}</ul>
                        <div class="rh-topright text-muted small">
                            <span class="cursor-pointer rh-minibtn" onclick="moveQuestion(${element.id}, 'up')">&#x25BC;</span>
                            <span class="cursor-pointer rh-minibtn" onclick="moveQuestion(${element.id}, 'down')">&#x25B2;</span>
                            <span class="cursor-pointer rh-minibtn" onclick="deleteQuestionHandler(${element.id})">X</span>
                        </div>`
    document.querySelector('#question_list').append(question)
}

function getTool() {
    document.querySelector('#question_list').innerHTML = "";
    // Fetch them tools
    const path = window.location.pathname.split('/');
    const id = path[2]
    fetch(`/api/get_complete_tool/${id}`)
    .then(response => response.json())
    .then(result => {
        // console.log(result)
        const tool = JSON.parse(result.tool)[0];
        const questions = result.questions
        document.querySelector('#tool_name').innerHTML = tool.fields.name;
        document.querySelector('#tool_desc').innerHTML = tool.fields.desc;
        questions.forEach(element => {
            writeQuestion(element); 
        })
    })
    .catch(() => {document.querySelector('#tool_name').innerHTML = "Jammer :(";}

    )

};