// Function to start session
async function startSession() {
    // Get the username input element from the DOM
    const usernameInput = document.getElementById("username");
    if (!usernameInput) return;  // If the username input is not found, return

    const username = usernameInput.value.trim();  // Trim any whitespace from the input
    if (!username) {
        alert("אנא הזן שם כדי להמשיך.");  // If no username is provided, alert the user
        return;
    }

    // Send the username to the backend for saving
    const success = await sendUsernameToBackend(username);
    if (!success) {
        alert("שגיאה בשמירת שם המשתמש. אנא נסה שוב.");  // If there's an error saving the username, alert the user
        return;
    }

    // Successfully saved username, hide the name input and show the app content
    const nameInputContainer = document.getElementById("name-input-container");
    if (nameInputContainer) nameInputContainer.style.display = "none";  // Hide the input container

    const appTitle = document.getElementById("app-title");
    if (appTitle) appTitle.style.display = "block";  // Show the app title

    const pdfCanvas = document.getElementById("pdfCanvas");
    if (pdfCanvas) pdfCanvas.style.display = "block";  // Show the PDF canvas

    const controls = document.querySelector(".controls");
    if (controls) controls.style.display = "block";  // Show the control elements

    const readingInfo = document.getElementById("reading-info");
    if (readingInfo) readingInfo.style.display = "block";  // Show the reading info section
}

// Function to send username to backend
async function sendUsernameToBackend(username) {
    const backendServiceUrl = 'http://localhost:5001/save_username_in_session';  // Define the backend URL

    try {
        // Send a POST request with the username to the backend
        const response = await fetch(backendServiceUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',  // Specify the content type as JSON
            },
            body: JSON.stringify({ username }),  // Send the username in the request body
        });

        const data = await response.json();  // Parse the response to JSON
        return response.ok;  // Return true if the request was successful
    } catch (error) {
        return false;  // Return false if there's an error communicating with the backend
    }
}

// Function to fetch and display data from the backend
async function fetchAndDisplayData() {
    const backendServiceUrl = `http://localhost:5001/get_all_data`;  // Define the backend URL

    try {
        const response = await fetch(backendServiceUrl);  // Make a GET request to fetch data
        const data = await response.json();  // Parse the response to JSON

        if (response.ok) {
            const dataContainer = document.getElementById("data-table").querySelector("tbody");
            dataContainer.innerHTML = "";  // Clear existing data from the table

            // Loop through the data and populate the table with rows
            data.forEach(row => {
                const rowElement = document.createElement("tr");  // Create a new table row element
                rowElement.innerHTML = `
                    <td>${row.id}</td>
                    <td>${row.username}</td>
                    <td>${row.page_number}</td>
                    <td>${row.time_spent}</td>
                    <td>${row.reading_speed}</td>
                `;
                dataContainer.appendChild(rowElement);  // Append the new row to the table
            });
        }
    } catch (error) {
        // Handle errors that might occur while fetching data
    }
}

// Function to start auto-refresh of data every 10 seconds
function startAutoRefresh() {
    setInterval(() => {
        fetchAndDisplayData();  // Call fetchAndDisplayData every 10 seconds to refresh the data
    }, 10000);  // 10 seconds refresh interval
}

// Function to clean the database by deleting all data
async function cleanDatabase() {
    const backendServiceUrl = 'http://localhost:5001/delete_all_data';  // Define the backend URL

    try {
        const response = await fetch(backendServiceUrl, { method: 'POST' });  // Send a POST request to delete all data
        const result = await response.json();  // Parse the response to JSON
        if (response.ok) {
            alert("All data has been deleted!");  // Alert the user that the data has been deleted successfully
            fetchAndDisplayData();  // Refresh the data after cleaning the database
        }
    } catch (error) {
        // Handle errors that might occur while cleaning the database
    }
}

// Event listener for DOM content loaded
document.addEventListener('DOMContentLoaded', () => {
    // Initialize start session button and add click event listener
    const startSessionButton = document.getElementById("start-session");
    if (startSessionButton) {
        startSessionButton.addEventListener("click", startSession);  // Start session when button is clicked
    }

    const url = 'some_pdf.pdf';  // URL to load the PDF document
    let pdfDoc = null;
    let currentPage = 1;
    let startTime = Date.now();  // Start time for the session

    // Load the PDF document using pdfjs library
    pdfjsLib.getDocument(url).promise.then(pdf => {
        pdfDoc = pdf;
        document.getElementById('totalPages').innerText = pdf.numPages;  // Display total number of pages in the PDF
        renderPage(currentPage);  // Render the first page
    }).catch(error => {
        // Handle error loading PDF
    });

    // Function to render a specific page of the PDF
    function renderPage(pageNum) {
        pdfDoc.getPage(pageNum).then(page => {
            const canvas = document.getElementById('pdfCanvas');
            const context = canvas.getContext('2d');
            const viewport = page.getViewport({ scale: 1.5 });

            canvas.height = viewport.height;
            canvas.width = viewport.width;

            // Render the PDF page on the canvas
            page.render({ canvasContext: context, viewport }).promise.catch(console.error);

            // Update word count and page number
            page.getTextContent().then(textContent => {
                const wordCount = textContent.items.map(item => item.str).join(' ').split(/\s+/).filter(word => word.length > 0).length;
                document.getElementById('wordCount').innerText = wordCount;  // Display word count
                document.getElementById('currentPage').innerText = pageNum;  // Update current page number
            }).catch(console.error);
        }).catch(console.error);
    }

    // Calculate time spent on the current page
    function calculateTimeSpent() {
        const endTime = Date.now();
        const timeSpent = ((endTime - startTime) / 1000).toFixed(2);  // Calculate time spent in seconds
        startTime = endTime;  // Update the start time for the next page
        return timeSpent;
    }

    // Page navigation event listeners
    document.getElementById('prevPage').addEventListener('click', () => {
        if (currentPage > 1) renderPage(--currentPage);  // Go to the previous page
    });

    document.getElementById('nextPage').addEventListener('click', async () => {
        if (currentPage < pdfDoc.numPages) {
            const timeSpent = calculateTimeSpent();  // Calculate time spent on the current page
            const wordCount = parseInt(document.getElementById('wordCount').innerText, 10);  // Get word count from the page
            await calculateReadingSpeedBackend(currentPage, timeSpent, wordCount);  // Send data to backend for speed calculation
            renderPage(++currentPage);  // Go to the next page
        }
    });

    // Function to calculate and send reading speed data to the backend
    async function calculateReadingSpeedBackend(page, timeSpent, wordCount) {
        try {
            const response = await fetch('http://localhost:5001/calculate_speed', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ page, time_spent: timeSpent, word_count: wordCount }),
            });

            const data = await response.json();
            return response.ok ? data.reading_speed : 0;  // Return reading speed if successful
        } catch {
            return 0;  // Return 0 if there's an error communicating with the backend
        }
    }

    // Initial fetch and auto-refresh
    fetchAndDisplayData();
    startAutoRefresh();
});
