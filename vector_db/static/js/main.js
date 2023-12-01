const searchBtn = document.getElementById('searchBtn');
const embeddingBtn = document.getElementById('embeddingBtn');
const addBtn = document.getElementById('addBtn');
const searchText = document.getElementById('searchText');
const resultsBox = document.getElementById('results');


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
    console.log(result);
    resultsBox.replaceChildren();
    for (const [index, value] of result['distances'][0].entries()) {
        console.log(index)
        li = document.createElement('li');
        li.classList.add('list-group-item');
        li.innerHTML = `${value} ${result['documents'][0][index]}`;
        resultsBox.appendChild(li);
    }
})
