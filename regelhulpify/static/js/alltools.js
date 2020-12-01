document.addEventListener('DOMContentLoaded', (event) => {
    getAllTools();
});

function getAllTools() {
    // Fetch them tools
    fetch(`/api/get_tools`)
    .then(response => response.json())
    .then(result => {
        const tools = JSON.parse(result);
        // Reset
        document.querySelector('#tools_list').innerHTML = "";
        tools.forEach(element => {
            createToolsBtn(element)
        });   
    });
}

