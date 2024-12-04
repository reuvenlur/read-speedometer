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
    const timeSpent = calculateTimeSpent();
    alert(`Time spent on page ${currentPage}: ${timeSpent} seconds`);
    currentPage--;
    renderPage(currentPage);
});

// ניווט לעמוד הבא
document.getElementById('nextPage').addEventListener('click', () => {
    if (currentPage >= pdfDoc.numPages) return;
    const timeSpent = calculateTimeSpent();
    alert(`Time spent on page ${currentPage}: ${timeSpent} seconds`);
    currentPage++;
    renderPage(currentPage);
});
