console.log("main.js is loaded");

import { fetchData } from "./api.js";
import { renderTable } from "./ui.js";

async function loadAndRenderData() {

    const tableName = "users";
    const tableSelector = "#dataTable";

    try {
        const data = await fetchData(tableName);
        renderTable(data, tableSelector);
    }

    catch(error) {
        console.error(`Failed to load or render data ${error}`);
    }
};

window.onload = loadAndRenderData;
    
