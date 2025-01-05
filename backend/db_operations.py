from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database credentials from .env file
user = os.getenv('DATABASE_USER', 'root')
password = os.getenv('DATABASE_PASSWORD', 'example')
host = os.getenv('DATABASE_HOST', 'localhost')
port = int(os.getenv('DATABASE_INTERNAL_PORT', 3306))
database = os.getenv('DATABASE_NAME', 'read_speedometer')

# Get SQLAlchemy connection
def get_connection():
    try:
        url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
        engine = create_engine(url)
        return engine
    except Exception as e:
        raise

# Insert data into the table
def save_page_data(engine, username, page_number, time_spent, reading_speed):
    try:
        with engine.begin() as connection:
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
            return {"message": "Data saved successfully!"}
    except Exception as e:
        return {"error": str(e)}

# Read data from the table
def read_table_data(engine):
    try:
        with engine.begin() as connection:
            query = text("SELECT * FROM page_data")
            result = connection.execute(query)
            rows = [dict(row) for row in result]
            return rows
    except Exception as e:
        return {"error": str(e)}

# Delete all data from the table
def delete_all_data(engine):
    try:
        with engine.begin() as connection:
            query = text("DELETE FROM page_data")
            connection.execute(query)
            return {"message": "All data deleted successfully!"}
    except Exception as e:
        return {"error": str(e)}
