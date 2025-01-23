export async function fetchData(tableName) {

    const urlApi = `http://localhost:8000/${endpoint}/`;
    
    try {
        const response = await fetch(urlApi);
        if (response.ok) {
            const data = await response.json();
            console.log("Fetched data:", data)
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