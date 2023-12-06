const searchBtn = document.getElementById('searchBtn');
const embeddingBtn = document.getElementById('embeddingBtn');
const addBtn = document.getElementById('addBtn');
const searchText = document.getElementById('searchText');
const resultsBox = document.getElementById('results');
const accordion = document.getElementById('accordion');


host = '127.0.0.1';
port = '8000';
url = `${host}:${port}`;

data = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: {}
}

addBtn.addEventListener('click', async () => {
    data.body = JSON.stringify({text: searchText.value});
    await fetch(`add/`, data);
})

embeddingBtn.addEventListener('click', async () => {
    data.body = JSON.stringify({text: searchText.value});
    let res = await fetch(`embedding/`, data);
    const result = await res.json();
    console.log(result);
    resultsBox.innerHTML = result;
})

searchBtn.addEventListener('click', async () => {
    data.body = JSON.stringify({text: searchText.value});
    let res = await fetch(`query/`, data);
    const result = await res.json();
    accordion.replaceChildren();
    update_accordion(accordion, result)
})

function update_accordion(accordion, results = []) {
    for (const [index, value] of results['distances'][0].entries()) {
        accordionItem = document.createElement('div');
        accordionItem.classList.add('accordion-item');
        collapseId = `collapse${index}`
        headerId = `heading${index}`

        // h2
        accordionHeader = document.createElement('h2');
        accordionHeader.classList.add('accordion-header');
        accordionHeader.setAttribute('id', headerId);

        accordionButton = document.createElement('button');
        accordionButton.classList.add('accordion-button'); 
        if (index != 0) { 
            accordionButton.classList.add('collapsed');
        };     
        accordionButton.setAttribute('type', 'button');  
        accordionButton.setAttribute('data-bs-toggle', 'collapse');  
        accordionButton.setAttribute('data-bs-target', `#${collapseId}`);
        if (index === 0) {
            accordionButton.setAttribute('aria-expanded', 'true'); 
        } else {
            accordionButton.setAttribute('aria-expanded', 'false'); 
        };
        accordionButton.setAttribute('aria-controls', collapseId);
        accordionButton.innerHTML = value;
        accordionHeader.appendChild(accordionButton);

        // collapse
        accordionCollapse = document.createElement('div');
        accordionCollapse.setAttribute('id', collapseId);
        accordionCollapse.classList.add('accordion-collapse');
        accordionCollapse.classList.add('collapse');
        if (index === 0) {
            accordionCollapse.classList.add('show');
            
        };
        accordionCollapse.setAttribute('aria-labelledby', headerId);
        accordionCollapse.setAttribute('data-bs-parent', 'accordion');
        accordionBody = document.createElement('div');
        accordionBody.classList.add('accordion-body');
        accordionBody.innerHTML = results['documents'][0][index];
        accordionCollapse.appendChild(accordionBody);


        accordionItem.appendChild(accordionHeader);
        accordionItem.appendChild(accordionCollapse);
        accordion.appendChild(accordionItem);
    }
}
