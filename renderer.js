const { ipcRenderer } = require('electron');

document.getElementById('fetchData').addEventListener('click', () => {
    const auditorEIN = document.getElementById('auditorEIN').value;
    const auditYear = document.getElementById('auditYear').value;
    ipcRenderer.send('fetch-data', { auditorEIN, auditYear });
});

ipcRenderer.on('data-response', (event, results) => {
    const resultsTable = document.getElementById('resultsTable').querySelector('tbody');
    resultsTable.innerHTML = ''; // Clear previous results

    results.forEach(result => {
        const tr = document.createElement('tr');
        Object.entries(result).forEach(([key, value]) => {
            const td = document.createElement('td');
            td.textContent = value;
            tr.appendChild(td);
        });
        resultsTable.appendChild(tr);
    });
});
