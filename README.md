# Read Speedometer
Application for analyzing reading data and measuring reading speed in WPM (words per minutes).

# Project Structure
pycache
    database_interface.cpython-312.py
backend
    server.py
    DB_operations.py
    Dockerfile
    requirements.txt
frontend
    index.html
    app.js
    styles.css
    Dockerfile
    some_pdf.pdf
screenshots
    1_start_page.jpg
    2_typing_name.jpg
    3_PDF_view.jpg
    4_navigation_buttons,_data_table,_and_data_delete_button.jpg
    5_data_is_updated_in_the_table_after_browsing_forward.jpg
    6_data_deletion.jpg
    7_after_deletion.png
.env
docker-compose.yml
init.sql
README.md


# Instructions
1. Ensure you have Docker installed

2. Clone the Repository
git clone https://github.com/yourusername/read-speedometer.git

3. Go to project folder
cd read-speedometer

4. Build the application
docker-compose up --build -d

5. Open the browser and access the URL
http://localhost:3000


# Application Screenshots
### 1. Start Page
<img src="screenshots/1_start_page.jpg" alt="Start Page" width="300" style="margin-bottom: 20px; display: block; margin-left: 0;" />

### 2. Typing Name
<img src="screenshots/2_typing_name.jpg" alt="Typing Name" width="300" style="margin-bottom: 20px; display: block; margin-left: 0;" />

### 3. PDF View
<img src="screenshots/3_PDF_view.jpg" alt="PDF View" width="300" style="margin-bottom: 20px; display: block; margin-left: 0;" />

### 4. Navigation Buttons, Data Table, and Data Delete Button
<img src="screenshots/4_navigation_buttons,_data_table,_and_data_delete_button.jpg" alt="Navigation Buttons and Table" width="300" style="margin-bottom: 20px; display: block; margin-left: 0;" />

### 5. Data Update After Navigation
<img src="screenshots/5_data_is_updated_in_the_table_after_browsing_forward.jpg" alt="Data Updated" width="300" style="margin-bottom: 20px; display: block; margin-left: 0;" />

### 6. Data Deletion
<img src="screenshots/6_data_deletion.jpg" alt="Data Deletion" width="300" style="margin-bottom: 20px; display: block; margin-left: 0;" />

### 7. After Data Deletion
<img src="screenshots/7_after_deletion.png" alt="After Deletion" width="300" style="margin-bottom: 20px; display: block; margin-left: 0;" />
