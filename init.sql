CREATE TABLE IF NOT EXISTS page_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    page_number INT,
    time_spent FLOAT,
    reading_speed FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
