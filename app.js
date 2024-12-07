const url = 'example.pdf'; // URL of the PDF file

let pdfDoc = null;
let currentPage = 1;
let startTime = Date.now(); // Start time for calculating time spent on a page

// Load the PDF document
pdfjsLib.getDocument(url).promise.then((pdf) => {
    console.log(`PDF loaded successfully. Total pages: ${pdf.numPages}`);
    pdfDoc = pdf;
    document.getElementById('totalPages').innerText = pdf.numPages;

    renderPage(currentPage); // Render the first page
}).catch(error => {
    console.error("Error loading PDF:", error);
});

// Function to render a specific page
function renderPage(pageNum) {
    console.log(`Rendering page: ${pageNum}`);
    pdfDoc.getPage(pageNum).then((page) => {
        const canvas = document.getElementById('pdfCanvas');
        const context = canvas.getContext('2d');
        const viewport = page.getViewport({ scale: 1.5 });

        canvas.height = viewport.height;
        canvas.width = viewport.width;

        // Render the page on the canvas
        page.render({
            canvasContext: context,
            viewport: viewport,
        }).promise.then(() => {
            console.log(`Page ${pageNum} rendered successfully.`);
        }).catch(error => {
            console.error(`Error rendering page ${pageNum}:`, error);
        });

        // Extract text content and calculate word count
        page.getTextContent().then((textContent) => {
            const pageText = textContent.items.map((item) => item.str).join(' ');
            const wordCount = pageText.split(/\s+/).filter(word => word.length > 0).length;

            console.log(`Page ${pageNum}: Word count calculated: ${wordCount}`);
            document.getElementById('wordCount').innerText = wordCount;
            document.getElementById('currentPage').innerText = pageNum;
        }).catch(error => {
            console.error(`Error extracting text from page ${pageNum}:`, error);
        });
    }).catch(error => {
        console.error(`Error loading page ${pageNum}:`, error);
    });
}

// Function to calculate the time spent on the current page
function calculateTimeSpent() {
    const endTime = Date.now(); // End time for the page
    const timeSpent = ((endTime - startTime) / 1000).toFixed(2); // Calculate time spent in seconds
    console.log(`Time spent on page ${currentPage}: ${timeSpent} seconds`);
    startTime = endTime; // Reset start time for the next page
    return timeSpent;
}

// Navigate to the previous page
document.getElementById('prevPage').addEventListener('click', () => {
    if (currentPage <= 1) {
        console.warn("Already on the first page. Cannot navigate further back.");
        return;
    }
    currentPage--;
    console.log(`Navigating to previous page: ${currentPage}`);
    renderPage(currentPage);
});

// Navigate to the next page
document.getElementById('nextPage').addEventListener('click', async () => {
    if (currentPage >= pdfDoc.numPages) {
        console.warn("Already on the last page. Cannot navigate further forward.");
        return;
    }

    const timeSpent = calculateTimeSpent(); // Calculate time spent on the current page
    const wordCount = parseInt(document.getElementById('wordCount').innerText, 10); // Get word count

    console.log(`Sending data to backend for page ${currentPage}: Time spent = ${timeSpent}, Word count = ${wordCount}`);

    // Send data to backend and get reading speed
    const readingSpeed = await calculateReadingSpeedBackend(currentPage, timeSpent, wordCount);

    console.log(`Backend response for page ${currentPage}: Reading speed = ${readingSpeed} words per minute`);

    // Update info box at the bottom
    document.getElementById('reading-info').innerText = `
        Time spent on page ${currentPage}: ${timeSpent} seconds
        Word count: ${wordCount}
        Reading speed: ${readingSpeed} words per minute
    `;

    currentPage++; // Advance to the next page
    console.log(`Navigating to next page: ${currentPage}`);
    renderPage(currentPage); // Render the next page
});

// Function to calculate reading speed by communicating with the backend
async function calculateReadingSpeedBackend(page, timeSpent, wordCount) {
    try {
        const response = await fetch('http://127.0.0.1:5000/calculate_speed', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                page: page, // Include page number
                time_spent: timeSpent,
                word_count: wordCount,
            }),
        });

        const data = await response.json();
        if (response.ok) {
            console.log("Backend calculation successful:", data);
            return data.reading_speed;
        } else {
            console.error("Backend error:", data.error);
            return 0;
        }
    } catch (error) {
        console.error("Error communicating with the backend:", error);
        return 0;
    }
}
