from sqlalchemy import create_engine, text
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - DatabaseInterface - %(message)s')

# Database credentials
user = 'root'
password = 'ReuvenMySQL123*'
host = '127.0.0.1'
port = 3306
database = 'reed_speedometer'

# Get SQLAlchemy connection
def get_connection():
    return create_engine(
        url=f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    )

# Insert data into the table
def save_page_data(engine, username, page_number, time_spent, reading_speed):
    try:
        with engine.connect() as connection:
            query = text("""
                INSERT INTO page_data (username, page_number, time_spent, reading_speed)
                VALUES (:username, :page_number, :time_spent, :reading_speed)
            """)
            connection.execute(query, {
                "username": username,
                "page_number": page_number,
                "time_spent": time_spent,
                "reading_speed": reading_speed
            })
            connection.commit()
            logging.info(f"Data saved successfully: User={username}, Page={page_number}, Time={time_spent}, Speed={reading_speed}")
            return {"message": "Data saved successfully!"}
    except Exception as e:
        logging.error(f"Error saving data: {e}")
        return {"error": str(e)}

# Read data from the table
def read_table_data(engine):
    try:
        with engine.connect() as connection:
            query = text("SELECT * FROM page_data")
            result = connection.execute(query)
            rows = [row for row in result]
            logging.info(f"Data retrieved from the database: {rows}")
            return rows
    except Exception as e:
        logging.error(f"Error reading data: {e}")
        return {"error": str(e)}
