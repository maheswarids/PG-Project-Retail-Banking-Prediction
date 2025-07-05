import psycopg2
import os
print("Current working directory:", os.getcwd())

# Function to convert model file to binary
def convert_model_to_binary(file_path):
    with open(file_path, "rb") as file:
        binary_data = file.read()
    return binary_data

# Convert the saved model file to binary format
binary_model = convert_model_to_binary(r"C:\PG Project\Banking_predictions\random_forest_model.pkl")

# Database connection details (for local PostgreSQL server)
db_params = {
    "host": "127.0.0.1",  # Local PostgreSQL host
    "database": "banking_predictions",  # Your database name
    "user": "postgres",  # Your PostgreSQL username
    "password": "mahe06",  # Your PostgreSQL password
    "port": "5432"  # Default PostgreSQL port
}

# Connect to PostgreSQL and insert model into the database
try:
    # Establish the connection
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    # SQL Query to insert the model into the table
    insert_query = """
    INSERT INTO model_storage (model_name, model_data)
    VALUES (%s, %s)
    """
    cursor.execute(insert_query, ("RandomForest_Model", psycopg2.Binary(binary_model)))

    # Commit the transaction
    conn.commit()
    print("✅ Model successfully inserted into PostgreSQL!")

except Exception as e:
    print("❌ Error:", e)

finally:
    # Close the cursor and connection
    cursor.close()
    conn.close()
