        function deleteAnswerHandler() {
            let pathArray = window.location.pathname.split('/');
            const answer_id = pathArray[4];
            console.log(pathArray.pop())
            const returnPath = pathArray.join('/')
            console.log(returnPath)
            
            
            fetch('/api/answer_delete/' + answer_id, {
                method: 'delete'
            })
            .then(response => console.log(response))
            .then(()=> { window.location.href = returnPath });
            
            
        }

        document.addEventListener('DOMContentLoaded', (event) => {
            document.querySelector('#answer_delete').addEventListener('click', deleteAnswerHandler);
        });