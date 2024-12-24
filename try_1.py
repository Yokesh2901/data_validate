import streamlit as st
import pandas as pd
import re

# Function to validate data
def validate_data(row, serial_numbers):
    errors = []
    
    # Check for missing values
    if pd.isnull(row['DOB']):
        errors.append("DOB is missing")
    if pd.isnull(row['father_name']):
        errors.append("Father's name is missing")
    if pd.isnull(row['serial_number']):
        errors.append("Serial number is missing")
    if pd.isnull(row['qualification']):
        errors.append("Qualification is missing")
    
    # Validate DOB format (date format check)
    if not pd.isnull(row['DOB']):
        try:
            pd.to_datetime(row['DOB'], format='%Y-%m-%d')
        except Exception:
            errors.append("DOB format is incorrect, should be YYYY-MM-DD")
    
    # Validate serial number (should be numeric)
    if not pd.isnull(row['serial_number']):
        if not str(row['serial_number']).isdigit():
            errors.append("Serial number must be numeric")
        elif row['serial_number'] in serial_numbers:
            errors.append("Serial number must be unique")
        else:
            serial_numbers.add(row['serial_number'])
    
    return errors

# Streamlit frontend
def main():
    st.title("Employee Data Input and Validation")

    # Upload file
    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)

        # Initialize a set to keep track of serial numbers
        serial_numbers = set()

        # Add a column to track validation errors
        df['errors'] = df.apply(lambda row: validate_data(row, serial_numbers), axis=1)

        # Display invalid rows
        invalid_rows = df[df['errors'].apply(lambda x: len(x) > 0)]
        
        if not invalid_rows.empty:
            st.write("Invalid data found in the following rows:")
            st.write(invalid_rows[['DOB', 'father_name', 'serial_number', 'qualification', 'errors']])
        else:
            st.success("All data is valid.")

if __name__ == "__main__":
    main()
