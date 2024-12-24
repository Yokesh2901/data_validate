import streamlit as st
import pandas as pd
import re

# Function to validate data for a single row
def validate_data(row, serial_numbers):
    errors = []
    
    # Check for missing values
    missing_values = {
        'DOB': "DOB is missing",
        'father_name': "Father's name is missing",
        'serial_number': "Serial number is missing",
        'qualification': "Qualification is missing"
    }
    
    for column, error_message in missing_values.items():
        if pd.isnull(row[column]):
            errors.append(error_message)

    # Validate DOB format (date format check)
    if not pd.isnull(row['DOB']):
        try:
            pd.to_datetime(row['DOB'], format='%Y-%m-%d')
        except Exception:
            errors.append("DOB format is incorrect, should be YYYY-MM-DD")
    
    # Validate serial number
    if not pd.isnull(row['serial_number']):
        if not str(row['serial_number']).isdigit():
            errors.append("Serial number must be numeric")
        elif row['serial_number'] in serial_numbers:
            errors.append("Serial number must be unique")
        else:
            serial_numbers.add(row['serial_number'])

    # Validate qualification (should be a string with only alphabets)
    if isinstance(row['qualification'], str):
        if not re.match(r'^[a-zA-Z]+$', row['qualification']):
            errors.append("Qualification must only contain alphabetic characters")
    else:
        errors.append("Qualification must be a string")
    
    return errors

# Streamlit frontend
def main():
    st.title("Employee Data Input and Validation")

    # File upload
    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)

        # Initialize a set to track unique serial numbers
        serial_numbers = set()

        # Apply validation function and track errors
        df['errors'] = df.apply(lambda row: validate_data(row, serial_numbers), axis=1)

        # Filter out invalid rows
        invalid_rows = df[df['errors'].apply(len) > 0]
        
        # Display results
        if not invalid_rows.empty:
            st.write("Invalid data found in the following rows:")
            st.dataframe(invalid_rows[['DOB', 'father_name', 'serial_number', 'qualification', 'errors']])
        else:
            st.success("All data is valid.")

if __name__ == "__main__":
    main()
