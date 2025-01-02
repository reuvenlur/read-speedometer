from sqlalchemy import create_engine, text
# import logging
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure logging
# logger = logging.getLogger('DatabaseInterface')
# logger.setLevel(logging.INFO)  # Reduced verbosity to INFO level
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - [MY_LOG] - DatabaseInterface - %(message)s')
# ch = logging.StreamHandler()
# ch.setFormatter(formatter)
# logger.addHandler(ch)

# Database credentials from .env file
user = os.getenv('DATABASE_USER', 'root')  # Default to 'root' if not defined
password = os.getenv('DATABASE_PASSWORD', 'example')  # Default password
host = os.getenv('DATABASE_HOST', 'localhost')  # Default to localhost
port = int(os.getenv('DATABASE_INTERNAL_PORT', 3306))  # Use internal port for Docker Networking
database = os.getenv('DATABASE_NAME', 'read_speedometer')  # Default database name

# Get SQLAlchemy connection
def get_connection():
    try:
        url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
        engine = create_engine(url)
        # logger.info("[MY_LOG] Database connection created successfully.")
        return engine
    except Exception as e:
        # logger.error(f"[MY_LOG] Failed to create database connection: {e}")
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
            # logger.info(f"[MY_LOG] Data saved: User={username}, Page={page_number}")
            return {"message": "Data saved successfully!"}
    except Exception as e:
        # logger.error(f"[MY_LOG] Error while saving data to the database: {e}")
        return {"error": str(e)}

# Read data from the table
def read_table_data(engine):
    try:
        with engine.begin() as connection:
            query = text("SELECT * FROM page_data")
            result = connection.execute(query)
            rows = [dict(row) for row in result]
            # logger.info("[MY_LOG] Data retrieved from the database.")
            return rows
    except Exception as e:
        # logger.error(f"[MY_LOG] Error while reading data from the database: {e}")
        return {"error": str(e)}

# Delete all data from the table
def delete_all_data(engine):
    try:
        with engine.begin() as connection:
            query = text("DELETE FROM page_data")
            connection.execute(query)
            # logger.info("[MY_LOG] All data deleted from the table.")
            return {"message": "All data deleted successfully!"}
    except Exception as e:
        # logger.error(f"[MY_LOG] Error while deleting data from the database: {e}")
        return {"error": str(e)}
