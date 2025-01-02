// Function to start session
async function startSession() {
    // Attempting to start session
    const usernameInput = document.getElementById("username");
    if (!usernameInput) {
        // Username input element not found
        return;
    }

    const username = usernameInput.value.trim();
    if (!username) {
        // No username provided
        alert("אנא הזן שם כדי להמשיך.");
        return;
    }

    // Username provided: ${username}
    const success = await sendUsernameToBackend(username);
    if (!success) {
        alert("שגיאה בשמירת שם המשתמש. אנא נסה שוב.");
        return;
    }

    // Session started successfully
    const nameInputContainer = document.getElementById("name-input-container");
    if (nameInputContainer) {
        nameInputContainer.style.display = "none";
    }

    const appTitle = document.getElementById("app-title");
    if (appTitle) {
        appTitle.style.display = "block";
    } else {
        // App title element not found
    }

    const pdfCanvas = document.getElementById("pdfCanvas");
    if (pdfCanvas) {
        pdfCanvas.style.display = "block";
    }

    const controls = document.querySelector(".controls");
    if (controls) {
        controls.style.display = "block";
    }

    const readingInfo = document.getElementById("reading-info");
    if (readingInfo) {
        readingInfo.style.display = "block";
    }
}

// Function to send username to backend
async function sendUsernameToBackend(username) {
    const backendServiceUrl = 'http://localhost:5001/save_username_in_session';

    try {
        const response = await fetch(backendServiceUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username }),
        });

        const data = await response.json();
        if (response.ok) {
            // Username saved successfully
            return true;
        } else {
            // Backend error: ${data.error}
            return false;
        }
    } catch (error) {
        // Error communicating with the backend
        return false;
    }
}

// Function to fetch and display data
async function fetchAndDisplayData() {
    // Fetching data from backend
    const backendServiceUrl = `http://localhost:5001/get_all_data`;

    try {
        const response = await fetch(backendServiceUrl);
        const data = await response.json();

        if (response.ok) {
            // Data fetched successfully
            const dataContainer = document.getElementById("data-table").querySelector("tbody");
            dataContainer.innerHTML = "";

            data.forEach(row => {
                const rowElement = document.createElement("tr");
                rowElement.innerHTML = `
                    <td>${row.id}</td>
                    <td>${row.username}</td>
                    <td>${row.page_number}</td>
                    <td>${row.time_spent}</td>
                    <td>${row.reading_speed}</td>
                `;
                dataContainer.appendChild(rowElement);
            });
        } else {
            // Error fetching data: ${data.error}
        }
    } catch (error) {
        // Error communicating with the backend
    }
}

// Function to start auto-refresh
function startAutoRefresh() {
    // Starting auto-refresh
    setInterval(() => {
        fetchAndDisplayData();
    }, 10000);
}

// Function to clean database
async function cleanDatabase() {
    // Cleaning database
    const backendServiceUrl = 'http://localhost:5001/delete_all_data';

    try {
        const response = await fetch(backendServiceUrl, { method: 'POST' });
        const result = await response.json();
        if (response.ok) {
            // Database cleaned successfully
            alert("All data has been deleted!");
            fetchAndDisplayData();
        } else {
            // Error cleaning database: ${result.error}
        }
    } catch (error) {
        // Error communicating with the backend
    }
}

// Event listener for DOM content loaded
document.addEventListener('DOMContentLoaded', () => {
    // Initializing application
    const startSessionButton = document.getElementById("start-session");
    if (startSessionButton) {
        startSessionButton.addEventListener("click", startSession);
        // Start session button connected
    } else {
        // start-session button not found
    }

    const url = 'example.pdf';

    let pdfDoc = null;
    let currentPage = 1;
    let startTime = Date.now();

    pdfjsLib.getDocument(url).promise.then((pdf) => {
        // PDF loaded successfully. Total pages: ${pdf.numPages}
        pdfDoc = pdf;
        document.getElementById('totalPages').innerText = pdf.numPages;
        renderPage(currentPage);
    }).catch(error => {
        // Error loading PDF
    });

    function renderPage(pageNum) {
        // Rendering page ${pageNum}
        pdfDoc.getPage(pageNum).then((page) => {
            const canvas = document.getElementById('pdfCanvas');
            const context = canvas.getContext('2d');
            const viewport = page.getViewport({ scale: 1.5 });

            canvas.height = viewport.height;
            canvas.width = viewport.width;

            page.render({
                canvasContext: context,
                viewport: viewport,
            }).promise.catch(error => {
                // Error rendering page ${pageNum}
            });

            page.getTextContent().then((textContent) => {
                const wordCount = textContent.items.map((item) => item.str).join(' ').split(/\s+/).filter(word => word.length > 0).length;
                document.getElementById('wordCount').innerText = wordCount;
                document.getElementById('currentPage').innerText = pageNum;
            }).catch(error => {
                // Error extracting text from page ${pageNum}
            });
        }).catch(error => {
            // Error loading page ${pageNum}
        });
    }

    function calculateTimeSpent() {
        const endTime = Date.now();
        const timeSpent = ((endTime - startTime) / 1000).toFixed(2);
        // Time spent on page ${currentPage}: ${timeSpent} seconds
        startTime = endTime;
        return timeSpent;
    }

    document.getElementById('prevPage').addEventListener('click', () => {
        if (currentPage <= 1) return;
        currentPage--;
        // Navigating to previous page: ${currentPage}
        renderPage(currentPage);
    });

    document.getElementById('nextPage').addEventListener('click', async () => {
        if (currentPage >= pdfDoc.numPages) return;

        const timeSpent = calculateTimeSpent();
        const wordCount = parseInt(document.getElementById('wordCount').innerText, 10);

        // Saving reading data for page ${currentPage}: time spent = ${timeSpent}s, word count = ${wordCount}
        await calculateReadingSpeedBackend(currentPage, timeSpent, wordCount);

        currentPage++;
        // Navigating to next page: ${currentPage}
        renderPage(currentPage);
    });

    async function calculateReadingSpeedBackend(page, timeSpent, wordCount) {
        const backendServiceUrl = 'http://localhost:5001/calculate_speed';

        try {
            const response = await fetch(backendServiceUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    page: page,
                    time_spent: timeSpent,
                    word_count: wordCount,
                }),
            });

            const data = await response.json();
            if (response.ok) {
                // Reading speed calculated: ${data.reading_speed} WPM
                return data.reading_speed;
            } else {
                // Backend error: ${data.error}
                return 0;
            }
        } catch (error) {
            // Error communicating with the backend
            return 0;
        }
    }

    fetchAndDisplayData();
    startAutoRefresh();
});
