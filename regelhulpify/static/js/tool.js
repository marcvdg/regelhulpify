document.addEventListener('DOMContentLoaded', (event) => { 
    getToolstart();
});

function getToolstart() {
    // Fetch that tool
    const path = window.location.pathname.split('/');
    fetch(`/api/get_toolstart/${path[1]}/`)
    .then(response => response.json())
    .then(result => {
        document.querySelector('#tool_name').innerHTML = result.name;
        document.querySelector('#tool_desc').innerHTML = result.desc;
        if (result.img != null) {
            document.querySelector('#tool_img').innerHTML = `<img class="rounded mw-100 mb-4" src="${result.img}"></img>`;
        };
        document.querySelector('#start_button').addEventListener('click', () => {
            window.location.href = `/${path[1]}/${result.start}`
        })
    });
    
}

