document.addEventListener('DOMContentLoaded', (event) => {
    getQuestion();
});

function writeAnswer(element, tool){
    // Write line
    const answer = document.createElement('div');
    answer.className = 'answer-button my-2';
    answer.innerHTML = `<input type='button' class='btn btn-primary' value='${element.text}'>`
    answer.addEventListener('click', () => {window.location.href = `/${tool}/${element.nextquestion}`})
    document.querySelector('#answer_list').append(answer)
}

function getQuestion() {
    document.querySelector('#answer_list').innerHTML = "";
    // Fetch them tools
    const path = window.location.pathname.split('/');
    fetch(`/api/get_question/${path[2]}/`)
    .then(response => response.json())
    .then(result => {
        result = result.question;
        const answers = result.answers;
        document.querySelector('#question_text').innerHTML = result.text;
        document.querySelector('#question_expl').innerHTML = result.expl;
        document.querySelector('#back_button').addEventListener('click', () => {window.location.href = `/${path[1]}/`})
        answers.forEach(element => {
            writeAnswer(element, path[1]); 
        });   
    });

}