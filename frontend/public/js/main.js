console.log("main.js is loaded");

import { fetchData } from "./api.js";
import { renderTable } from "./ui.js";

async function loadTableData(endpoint, tableSelector) {

    try {
        const data = await fetchData(tableName);
        renderTable(data, tableSelector);
    } catch(error) {
        console.error(`Failed to load or render data ${error}`);
    }
};

document.getElementById("loadUsers").addEventListener("click", () => {
    loadTableData("users", "#usersTable");
});

document.getElementById("loadStaffs").addEventListener("click", () => {
    loadTableData("staffs", "#staffsTable");
});

document.getElementById("loadStudents").addEventListener("click", () => {
    loadTableData("students", "#studentsTable");
});

document.getElementById("loadRoles").addEventListener("click", () => {
    loadTableData("roles", "#rolesTable")
});

window.onload = loadAndRenderData;
    
