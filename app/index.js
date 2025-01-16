async function fetchData() {
    const tableName = 'users';
    const urlApi = `http://127.0.0.1:8000/${tableName}/`;

    try {
        const response = await fetch(urlApi);
        if (response.ok) {
            const data = await response.json();
            console.log(data)
    
        if (!data.length) {
            document.querySelector("#dataTable tbody").innerHTML = `
           <tr>
                <td colspan="3">There is no data to display</td>
           </tr> 
           `;
           return;
        }
        const tableHead = document.querySelector("#dataTable thead tr");
        tableHead.innerHTML = Object.keys(data[0]).map(key => `<th>${key}</th>`).join("");

        const tableBody = document.querySelector("#dataTable tbody");
        tableBody.innerHTML = data.map(record => {
            return `
            <tr>
                ${Object.values(record).map(value => `<td>${value}</td>`).join("")}
            </tr>
            `;
        }).join("");
    }
        else {
            throw new Error(`Error API ${error}`)
        }
        
    } catch (error) {
        console.error(`Receiving error data ${error}`);
    }
}


window.onload = fetchData;