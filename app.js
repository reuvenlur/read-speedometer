const url = 'example.pdf'; // URL של קובץ ה-PDF

let pdfDoc = null;
let currentPage = 1;
let startTime = Date.now(); 

// טוען את ה-PDF
pdfjsLib.getDocument(url).promise.then((pdf) => {
    pdfDoc = pdf;
    document.getElementById('totalPages').innerText = pdf.numPages;

    renderPage(currentPage);
});

// פונקציה לרינדור עמוד
function renderPage(pageNum) {
    pdfDoc.getPage(pageNum).then((page) => {
        const canvas = document.getElementById('pdfCanvas');
        const context = canvas.getContext('2d');
        const viewport = page.getViewport({ scale: 1.5 });

        canvas.height = viewport.height;
        canvas.width = viewport.width;

        // רינדור העמוד
        page.render({
            canvasContext: context,
            viewport: viewport,
        });

        // שליפת טקסט וחישוב כמות המילים
        page.getTextContent().then((textContent) => {
            const pageText = textContent.items.map((item) => item.str).join(' ');
            const wordCount = pageText.split(/\s+/).filter(word => word.length > 0).length;

            // עדכון נתוני תצוגה
            document.getElementById('wordCount').innerText = wordCount;
            document.getElementById('currentPage').innerText = pageNum;
        });
    });
}

function calculateTimeSpent() {
    const endTime = Date.now(); // זמן סיום
    const timeSpent = ((endTime - startTime) / 1000).toFixed(2); // חישוב שניות
    startTime = endTime; // עדכון זמן התחלה לעמוד החדש
    return timeSpent;
}

// ניווט לעמוד קודם
document.getElementById('prevPage').addEventListener('click', () => {
    if (currentPage <= 1) return;
    currentPage--;
    renderPage(currentPage);
});

// ניווט לעמוד הבא
document.getElementById('nextPage').addEventListener('click', async () => {
    if (currentPage >= pdfDoc.numPages) return;

    const timeSpent = calculateTimeSpent(); // Calculate time spent
    const wordCount = parseInt(document.getElementById('wordCount').innerText, 10); // Get word count

    // Send data to backend and get reading speed
    const readingSpeed = await calculateReadingSpeedBackend(timeSpent, wordCount);

    // Update info box at the bottom
    document.getElementById('reading-info').innerText = `
        Time spent on page ${currentPage}: ${timeSpent} seconds
        Word count: ${wordCount}
        Reading speed: ${readingSpeed} words per minute
    `;

    currentPage++; // Advance to the next page
    renderPage(currentPage); // Render the next page
});

async function calculateReadingSpeedBackend(timeSpent, wordCount) {
    const response = await fetch('http://127.0.0.1:5000/calculate_speed', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            time_spent: timeSpent,
            word_count: wordCount,
        }),
    });

    const data = await response.json();
    if (response.ok) {
        return data.reading_speed;
    } else {
        console.error(data.error);
        return 0;
    }
}