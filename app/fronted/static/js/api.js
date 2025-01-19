export async function fetchData(tableName) {

    const urlApi = `http://127.0.0.1:8000/${tableName}/`;
    
    try {
        const response = await fetch(urlApi);
        if (response.ok) {
            const data = await response.json();
            return data;
        }
        
        else {
            throw new Error(`Error API ${response.statusText}`);
            }
    }

    catch (error) {
        console.error(`Receiving error data ${error}`);
        throw error;
            }
}