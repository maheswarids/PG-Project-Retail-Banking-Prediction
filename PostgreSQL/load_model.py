import psycopg2
import pickle
import numpy 

# Database connection details
db_params = {
    "host": "localhost",  # Ensure PostgreSQL is running locally
    "database": "banking_predictions",
    "user": "postgres",  # Replace with your actual PostgreSQL username
    "password": "mahe06",  # Replace with your actual PostgreSQL password
    "port": "5432"  # Default PostgreSQL port
}

# Load the model from PostgreSQL
def load_model():
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # SQL Query to retrieve the model
        select_query = "SELECT model_data FROM model_storage WHERE model_name = %s"
        cursor.execute(select_query, ("RandomForest_Model",))
        model_data = cursor.fetchone()[0]

        # Load the model from the binary data
        model = pickle.loads(model_data)
        print("✅ Model loaded successfully!")

        # Now you can use the model to make predictions or further analysis
        # Example: model.predict(X_test)

    except Exception as e:
        print("❌ Error:", e)

    finally:
        cursor.close()
        conn.close()

# Run the load model function
load_model()
