import streamlit as st
import numpy as np
import pickle
import psycopg2

# Function to load the model from PostgreSQL
def load_model():
    db_params = {
        "host": "localhost",
        "database": "banking_predictions",
        "user": "postgres",
        "password": "mahe06",
        "port": "5432"
    }

    conn = None
    cursor = None

    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # SQL Query to retrieve the model
        select_query = "SELECT model_data FROM model_storage WHERE model_name = %s"
        cursor.execute(select_query, ("RandomForest_Model",))
        model_data = cursor.fetchone()[0]

        # Load the model from the binary data
        model = pickle.loads(model_data)
        print("Model loaded successfully!")
        return model

    except Exception as e:
        print("Error:", e)
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Streamlit UI
st.title("Term Deposit Prediction")

# User Inputs
age = st.number_input("Age", min_value=18, max_value=100)  # Age input as integer, no step
job = st.selectbox("Job Type", ['admin.', 'blue-collar', 'entrepreneur', 'housemaid', 'management', 'retired', 'self-employed', 'services', 'student', 'technician', 'unemployed', 'unknown'])
marital = st.selectbox("Marital Status", ['married', 'single', 'divorced'])
education = st.selectbox("Education Level", ['primary', 'secondary', 'tertiary', 'unknown'])
balance = st.number_input("Account Balance")  # Account balance input as integer, no step
loan = st.radio("Personal Loan", ['No', 'Yes'])
housing = st.radio("Housing Loan", ['No', 'Yes'])
default = st.radio("Credit in Default", ['No', 'Yes'])
previous = st.number_input("Number of Previous Contacts", min_value=0)  # Previous contacts input as integer, no step
poutcome = st.selectbox("Previous Campaign Outcome", ['failure', 'unknown', 'success'])
campaign = st.number_input("Number of Contacts During Campaign", min_value=1)  # Contacts during campaign input as integer, no step

# Additional inputs
contact = st.selectbox("Contact Type", ['cellular', 'telephone', 'unknown'])
day_of_last_contact = st.number_input("Day of Last Contact", min_value=1, max_value=31)  # Day input as integer, no step
pre_days = st.number_input("Days Since Last Contact (Pre-Days)", min_value=-1)  # Pre-days input as integer, no step
duration = st.number_input("Duration of Last Contact (in seconds)", min_value=1)  # Duration input as integer, no step
month_of_last_contact = st.text_input("Month of Last Contact")  # Month input as text

# Convert categorical inputs to numerical values
mapping = {'Yes': 1, 'No': 0}
loan = mapping[loan]
housing = mapping[housing]
default = mapping[default]

job_mapping = {j: i for i, j in enumerate(['admin.', 'blue-collar', 'entrepreneur', 'housemaid', 'management', 'retired', 'self-employed', 'services', 'student', 'technician', 'unemployed', 'unknown'])}
marital_mapping = {'married': 0, 'single': 1, 'divorced': 2}
education_mapping = {'primary': 0, 'secondary': 1, 'tertiary': 2, 'unknown': 3}
poutcome_mapping = {'failure': 0, 'unknown': 1, 'success': 2}
contact_mapping = {'cellular': 0, 'telephone': 1, 'unknown': 2}
month_mapping = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6, 'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12}

job = job_mapping[job]
marital = marital_mapping[marital]
education = education_mapping[education]
poutcome = poutcome_mapping[poutcome]
contact = contact_mapping[contact]
month_of_last_contact = month_mapping.get(month_of_last_contact.lower(), -1)  # Default to -1 if invalid month

# Prepare data for prediction
input_features = np.array([[age, job, marital, education, balance, loan, housing, default, previous, poutcome, campaign, contact, day_of_last_contact, pre_days, duration, month_of_last_contact]])

# Load model once when the page is loaded
model = load_model()

if st.button("Predict"):
  if model:
      prediction = model.predict(input_features)
      result = "The Customer will Accept the term Deposit" if prediction[0] == 1 else "The Customer will not Accept the term Deposit"
      st.success(f"Prediction: {result}")
else:
    st.error("Error loading the model.")


