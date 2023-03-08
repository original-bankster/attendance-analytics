import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Define file paths
attendance_names_path = 'Attendance_Names.csv'
attendance_record_path = 'Attendance_Record.csv'

# Load attendance names
attendance_names = pd.read_csv(attendance_names_path)

# Define the Streamlit app
def app():
    st.title('Attendance Management Tool')

    # Load the attendance record, or create an empty dataframe if it doesn't exist
    attendance_record = pd.read_csv(attendance_record_path) if os.path.isfile(attendance_record_path) else pd.DataFrame()

    # Convert Check-In Time and Check-Out Time columns to datetime objects
    attendance_record['Check-In Time'] = pd.to_datetime(attendance_record['Check-In Time'], errors='coerce')
    attendance_record['Check-Out Time'] = pd.to_datetime(attendance_record['Check-Out Time'], errors='coerce')

    # Define function to update status based on check-in and check-out times
    def update_status(row):
        if pd.isnull(row['Check-In Time']):
            return 'Not Checked In'
        elif pd.isnull(row['Check-Out Time']):
            return 'Checked In'
        elif pd.to_datetime(row['Check-In Time']) > pd.to_datetime(row['Check-Out Time']):
            return 'Checked In'
        else:
            return 'Checked Out'

    # Update status column
    attendance_record['Status'] = attendance_record.apply(update_status, axis=1)

    # Create a drop-down list for users to select their names
    selected_name = st.selectbox('Select your name:', attendance_names['Name'])

    # Get the selected row from the attendance names DataFrame
    selected_row = attendance_names.loc[attendance_names['Name'] == selected_name].iloc[0]

    # Display the project role, QC team, and company fields for the selected user
    st.write('Project Role:', selected_row['Project Role'])
    st.write('QC Team:', selected_row['QC Team'])
    st.write('Company:', selected_row['Company'])

    # Get the user's latest check-in/check-out event
    user_events = attendance_record.loc[attendance_record['Name'] == selected_name]
    user_latest_event = user_events.tail(1) if not user_events.empty else None

    # Check if user is already checked in
    if user_latest_event is not None and user_latest_event['Status'].item() == 'Checked In':
        checked_in = True
        check_in_time = user_latest_event['Check-In Time'].item().strftime('%I:%M:%S %p')
        check_out_time = ''
    else:
        checked_in = False
        check_in_time = ''
        check_out_time = ''

    # Check-in and check-out buttons
    if checked_in:
        st.write('You are checked in.')
        check_out = st.button('Check out')
        if check_out:
            # Record check-out event
            latest_event_id = user_latest_event['Event ID'].item() + 1 if not user_events.empty else 1
            attendance_record = attendance_record.append({'Name': selected_name, 'QC Team': selected_row['QC Team'], 'Project Role': selected_row['Project Role'], 'Company': selected_row['Company'], 'Event ID': latest_event_id,'Date': datetime.now().strftime('%Y-%m-%d'), 'Check-In Time': user_latest_event['Check-In Time'].item(), 'Check-Out Time': datetime.now()}, ignore_index=True)
            attendance_record.to_csv(attendance_record_path, index=False)
            st.write('You have checked out.')
    else:
        st.write('You are checked out.')
        check_in = st.button('Check in')
        if check_in:
            # Record check-in event
            latest_event_id = user_latest_event['Event ID'].item() + 1 if not user_events.empty else 1
            attendance_record = attendance_record.append({'Name': selected_name, 'QC Team': selected_row['QC Team'], 'Project Role': selected_row['Project Role'], 'Company': selected_row['Company'], 'Event ID': latest_event_id, 'Date': datetime.now().strftime('%Y-%m-%d'), 'Check-In Time': datetime.now(), 'Check-Out Time': pd.NaT}, ignore_index=True)
            attendance_record.to_csv('Attendance_Record.csv', index=False)
            st.write('You have checked in.')


if __name__ == '__main__':
    app()






