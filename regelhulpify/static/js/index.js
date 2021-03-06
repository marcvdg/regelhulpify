document.addEventListener('DOMContentLoaded', (event) => {
    getLatestTools();
});

function getLatestTools() {
    // Fetch them tools
    fetch(`/api/get_tools`)
    .then(response => response.json())
    .then(result => {
        const tools = JSON.parse(result);
        // Reset
        document.querySelector('#tools_list').innerHTML = "";
        const last3 = tools.splice(-3);
        last3.forEach(element => {
            createToolsBtn(element)
        });   
    });
}

