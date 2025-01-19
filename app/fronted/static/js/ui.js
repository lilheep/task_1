export function renderTable(data, tableSelector) {

    const table = document.querySelector(tableSelector);

    if (!data.length) {
        table.querySelector("tbody").innerHTML = `
           <tr>
                <td colspan="3">There is no data to display</td>
           </tr> 
           `;
           return;
    }

    const tableHead = table.querySelector("thead tr");
    tableHead.innerHTML = Object.keys(data[0]).map(key => `<th>${key}</th>`).join("");

    const tableBody = table.querySelector("tbody");
    tableBody.innerHTML = data.map(record => {
        return `
        <tr>
            ${Object.values(record).map(value => `<td>${value}</td>`).join("")}
        </tr>
        `;
    }).join("");
}
