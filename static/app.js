
const searchForm = document.getElementById("search-form");
const resultsTable = document.getElementById("results-table");
const documentText = document.getElementById("document-text");

searchForm.addEventListener("submit", (event) => {
    event.preventDefault(); // Prevent default form submission

    const query = document.getElementById("query").value;
    const model = document.getElementById("model").value;

    fetch(`/search?q=${query}&model=${model}`)
        .then(response => response.json())
        .then(results => {
            // Clear previous results
            resultsTable.innerHTML = "";
            documentText.innerHTML = "";

            // Populate table with results
            results.forEach(result => {
                const row = document.createElement("tr");
                const nameCell = row.insertCell();
                nameCell.textContent = result[0];
                const rankCell = row.insertCell();
                rankCell.textContent = result[1];
                row.addEventListener("click", () => {
                    // Fetch and display document text when row is clicked
                    fetch(`/document/${result[0]}`)
                        .then(response => response.text())
                        .then(text => {
                            documentText.textContent = text;
                            // Highlight matching terms (implement highlighting logic here)
                        });
                });
                resultsTable.appendChild(row);
            });
        });
});