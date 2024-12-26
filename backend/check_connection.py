from sqlalchemy import create_engine, text

# Database connection setup
DATABASE_URL = "mysql+mysqlconnector://root:ReuvenMySQL123*@localhost/reed_speedometer"
engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as connection:
        print("Connection successful!")
        
        # Start a transaction
        with connection.begin() as transaction:
            # Insert data into the table
            insert_query = text("""
                INSERT INTO page_data (username, page_number, time_spent, reading_speed)
                VALUES (:username, :page_number, :time_spent, :reading_speed)
            """)
            
            # Data to insert
            data = {
                "username": "test_user",
                "page_number": 1,
                "time_spent": 12.5,
                "reading_speed": 150.0
            }
            
            # Execute the query
            connection.execute(insert_query, parameters=data)
            print("Data inserted successfully!")
except Exception as e:
    print(f"Operation failed: {e}")
