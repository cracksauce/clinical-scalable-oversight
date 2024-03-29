import streamlit as st
import pandas as pd
import json
import tempfile
import os
import queue
import threading
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
from parallel_processing.prompts import v1_system_message, v1_prompt_message
from parallel_processing.generate_requests import generate_chat_completion_requests
from parallel_processing.main import main as parallel_processing_main
from parallel_processing.main import process_data
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Initialize logger for error tracking
logging.basicConfig(filename='app_errors.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize a Queue to manage the batch runs
batch_run_queue = queue.Queue()

# Initialize session state variables for UI elements and data selections
if 'manual_load_clicked' not in st.session_state:
    st.session_state['manual_load_clicked'] = False
if 'auto_load_clicked' not in st.session_state:
    st.session_state['auto_load_clicked'] = False
if 'batch_initiated' not in st.session_state:
    st.session_state['batch_initiated'] = False
if 'selected_data' not in st.session_state:
    st.session_state['selected_data'] = None
if 'manual_selection' not in st.session_state:
    st.session_state['manual_selection'] = False
if 'auto_selection' not in st.session_state:
    st.session_state['auto_selection'] = False
if 'selected_rows' not in st.session_state:
    st.session_state.selected_rows = []
if 'batch_status' not in st.session_state:
    st.session_state['batch_status'] = 'Not started'
if 'progress_bar' not in st.session_state:
    st.session_state['progress_bar'] = None
if 'log_messages' not in st.session_state:
    st.session_state['log_messages'] = []
if 'selected_mcqs_list' not in st.session_state:
    st.session_state['selected_mcqs_list'] = []
if 'batch_run_is_complete' not in st.session_state:
    st.session_state['batch_run_is_complete'] = False
if 'formatted_system_message' not in st.session_state:
    st.session_state['formatted_system_message'] = ""
if 'formatted_prompt' not in st.session_state:
    st.session_state['formatted_prompt'] = ""
     
# Other random initializations
data_file_path = ""
requests_file_path = ""
results_file_path = ""
output_file_path = ""

# Function to update the session state with selected rows
def update_selected_rows(selected_rows_data):
    st.session_state.selected_rows = selected_rows_data

def run_in_thread(fn, *args, **kwargs):
    """Run a function in a separate thread while maintaining Streamlit context."""
    def wrapped_fn():
        with st.script_run_ctx():
            fn(*args, **kwargs)
    threading.Thread(target=wrapped_fn).start()

# Function to normalize the dataframe structure
def normalize_df(df, vignette_type):
    column_name = None
    
    if vignette_type == 'Baseline':
        column_name = 'full_qa_no_demo'
    elif vignette_type == 'Customized':
        column_name = 'full_qa_w_placeholders'
    
    if column_name and column_name in df.columns:
        df = df.set_index(column_name)  # Set the column as index if you wish to select it later
    else:
        logging.error(f"Column {column_name} not found in DataFrame or vignette_type {vignette_type} is invalid.")
        st.error(f"An error occurred: Column {column_name} not found in DataFrame or vignette_type {vignette_type} is invalid.")
        return None

    return df

        
def process_batch_runs(batch_run_data):
    # Define the file paths within the function scope
    data_file_path = None
    requests_file_path = None
    results_file_path = None
    output_file_path = None
    while True:
        batch_run = batch_run_queue.get()
        if batch_run is None:
            # Signal the end of the queue and break the loop
            st.session_state['batch_run_is_complete'] = True  # Update the state here
            break
        
        try:
            # Now we're sure batch_run is not None, we can unpack it
            # ATTENTION ****!!!!""""Streamlit Documentation Expert Chatbot""""!!!!**** I NEED THIS PORTION OF CODE TO BE CHECKED AND CHANGED AS WE ARE CHANGING THE STRUCTURE OF HOW WE ARE 'CUSTOMIZING' PROMPTS IF USER SELECTS TO CUSTOMIZE VIGNETTES
            selected_mcqs_list, formatted_system_message, formatted_prompt = batch_run
            
            # Initialize progress
            total_tasks = len(selected_mcqs_list)
            completed_tasks = 0
                
            for task in selected_mcqs_list:
                # Simulate task processing (e.g., calling an API, processing data)
                # ...
                # Update task progress
                completed_tasks += 1
                progress = int((completed_tasks / total_tasks) * 100)
                st.session_state['progress'] = progress
                st.session_state['progress_bar'].progress(progress)
                
                # Update log messages periodically or upon certain events
                log_message = f"Completed task {completed_tasks} of {total_tasks}"
                st.session_state['log_messages'].append(log_message)
                st.session_state['log_output'].text('\n'.join(st.session_state['log_messages']))
            
                # Update completion message and status
                completion_message = f"Batch run completed. Results saved."
                st.session_state['log_messages'].append(completion_message)
                st.session_state['log_output'].text('\n'.join(st.session_state['log_messages']))
                st.session_state['batch_status'] = 'Completed'
                pass
        
        except Exception as e:
            error_message = f"Error occurred: {e}"
            st.session_state['log_messages'].append(error_message)
            st.session_state['log_output'].text('\n'.join(st.session_state['log_messages']))
            logging.error(error_message)
            st.session_state['batch_status'] = 'Failed'

        finally:
            batch_run_queue.task_done()

    # Indicate the batch run is complete
    if st.session_state['batch_run_is_complete']:
        st.session_state['batch_status'] = 'Completed'
        selected_mcqs_list, formatted_system_message, formatted_prompt = batch_run

        # Call the refactored parallel processing script
        parallel_processing_main.main(
            data=selected_mcqs_list,
            prompt=formatted_system_message + formatted_prompt,
            model_name=os.getenv('MODEL_NAME'),
            data_file_path=data_file_path,
            requests_file_path=requests_file_path,
            results_file_path=results_file_path,
            output_file_path=output_file_path
            )
        pass

def update_ui():
    # Update the Streamlit UI based on the progress
    # You will need to define the logic of this function based on your requirements
    # For example:
    st.session_state['progress_bar'].progress(st.session_state['progress'])
    st.session_state['log_output'].text('\n'.join(st.session_state['log_messages']))

# This function should update the state when manual questions are loaded
def manual_load():
    st.session_state['manual_load_clicked'] = True
    st.session_state['auto_load_clicked'] = False

# This function should update the state when auto questions are loaded
def auto_load():
    st.session_state['auto_load_clicked'] = True
    st.session_state['manual_load_clicked'] = False

# Function to split the dataframe into chunks with specified ranges
# ATTENTION ****!!!!""""Streamlit Documentation Expert Chatbot""""!!!!**** THIS NEEDS TO BE CHANGED AS I BROKE UP THE FILE INTO MULTIPLE DIFFERENT FILES (DETAILED BELOW)
# ATTENTION ****!!!!""""Streamlit Documentation Expert Chatbot""""!!!!**** i want each of the csv's to be broken down as follows:
# Questions 1 to 10 (n=10)
# Questions 11-20 (n=10)
# Questions 21-25 (n=5)
def get_question_ranges(df_length):
    ranges = [
        (1, 50, 'Questions 1 to 50 (n=50)'),
        (51, 100, 'Questions 51-100 (n=50)'),
        (101, 150, 'Questions 101-150 (n=50)'),
        (151, 200, 'Questions 151-200 (n=50)'),
        (201, 240, 'Questions 201-240 (n=40)'),
        (241, 270, 'Questions 241-270 (n=30)'),
        (271, 290, 'Questions 271-290 (n=20)'),
        (291, 305, 'Questions 291-305 (n=15)'),
        (306, 315, 'Questions 306-315 (n=10)'),
    ]
    return [(start, end, label) for start, end, label in ranges if start < df_length + 1]

# Load the CSV file into a pandas DataFrame
@st.cache_data
def load_data(filename):
    data = pd.read_csv(filename)
    return data

# Function where the normalization and column selection is called
def load_questions(vignette_type, df):
    normalized_df = normalize_df(df, vignette_type)
    if normalized_df is not None:
        return normalized_df
    else:
        st.error("Data normalization failed. Please check your data and vignette type selection.")
        return None

# The main function where we will build the app
def main():
    st.title("Clinical Knowledge MCQ Performance Eval")
    st.subheader("Do demographic features in patient vignettes influence LLM outputs due to intrinsic, algorithmic biases?")
    st.write("This toolkit allows for batch processing of high-quality multiple choice questions (MCQs) testing clinical knowledge and reasoning skills with customizable features to inject single or multiple demographic features into a vignette to assess for differences in outputs inputs and analyze performance differences.")
    
    # Dropdown for CSV file selection
    csv_options = {
        'Emergency Medicine MCQs': 'data/emerg-medicine.csv',
        'Family Medicine MCQs': 'data/fam-medicine.csv',
        'Internal Medicine MCQs': 'data/internal-medicine.csv',
        'Neurology MCQs': 'data/neurology.csv',
        'Ob/Gyn MCQs': 'data/obgyn.csv',
        'Pediatrics MCQs': 'data/pediatrics.csv',
        'Psychiatry MCQs': 'data/psychiatry.csv',
        'Surgery MCQs': 'data/surgery.csv',
    }
    selected_csv_label = st.selectbox('Select MCQ Category:', list(csv_options.keys()))
    csv_file_path = csv_options[selected_csv_label]

    # Get the selected vignette type from the user input
    vignette_type_options = ['Baseline', 'Customized']
    vignette_type = st.selectbox('Select Vignette Type:', vignette_type_options)

    # Load the data
    df = load_data(csv_file_path)
    
    # Mapping of user-friendly labels to expected values
    vignette_type_mapping = {
        'Baseline': 'full_qa_no_demo',  # Adjust the key to match exactly how it appears in the UI
        'Customized': 'full_qa_w_placeholders'  # Adjust the key to match exactly how it appears in the UI
    }
    
    # Initialize the variable at the start of your main function
    selected_mcqs_list = []

    # Manual Selection of MCQs
    st.subheader("Manual Select MCQs")
    if st.checkbox('Show spreadsheet of your selected MCQ subset'):
        # Create an interactive table using AgGrid for manual selection
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_selection('multiple', use_checkbox=True)  # Enable checkbox for multiple selection
        grid_options = gb.build()

        grid_response = AgGrid(
            df,
            gridOptions=grid_options,
            update_mode=GridUpdateMode.SELECTION_CHANGED,
            fit_columns_on_grid_load=True,
            height=300,
            width='100%',
            data_return_mode=DataReturnMode.AS_INPUT,
        )
        # Update the selected rows in the session state
        if grid_response['selected_rows']:
            update_selected_rows(grid_response['selected_rows'])

        # Check if any rows are selected
        if grid_response['selected_rows']:
            # Update session state with the selected data
            st.session_state['selected_data'] = pd.DataFrame(grid_response['selected_rows'])
            st.session_state['manual_selection'] = True  # Indicate manual selection is done
            st.session_state['auto_selection'] = False

   # Load manually selected questions and normalize the DataFrame
    if st.button('Load Manually Selected Questions'):
        manual_load()
        if st.session_state['manual_selection']:
            st.session_state['manual_load_clicked'] = True
            st.write("**😎 Your manual selection has been processed**")

            # Get the selected vignette type from the user input
            vignette_type = st.session_state.get('selected_vignette_type', 'Baseline')  # Default to 'Baseline' if not set

            # Normalize the dataframe based on the user's selection of vignette type
            normalized_df = normalize_df(st.session_state['selected_data'], vignette_type)
            
            # Check if the normalization returned a DataFrame
            if normalized_df is not None:
                # Determine the correct column name based on the selected vignette type
                expected_column = vignette_type_mapping.get(vignette_type)

                if expected_column in normalized_df.columns:
                    # Set the selected MCQs list in the session state
                    st.session_state['selected_mcqs_list'] = normalized_df[expected_column].tolist()
                else:
                    # Log the error and display an error message if the expected column is not found
                    logging.error(f"Expected column {expected_column} not found in the normalized DataFrame for vignette type {vignette_type}.")
                    st.error(f"An error occurred: Expected column {expected_column} not found for vignette type {vignette_type}. Please check your data and normalization process.")
            else:
                # Display an error message if normalization failed
                st.error("Data normalization failed. Please check your data and vignette type selection.")

    

    # Auto Selection of MCQs
    st.subheader("Auto Select MCQs")
    question_ranges = get_question_ranges(len(df))
    option_labels = [label for _, _, label in question_ranges]
    selected_label = st.selectbox("Select question range", options=option_labels)
    selected_range = next((start, end) for start, end, label in question_ranges if label == selected_label)

    # Button to load auto-selected questions
    if st.button('Load Auto Selected Questions'):
        auto_load()
        start_index = selected_range[0] - 1
        end_index = selected_range[1]
        if start_index is not None and end_index is not None:
            st.session_state['auto_selection'] = True
            st.session_state['auto_load_clicked'] = True  # Ensure this is set here
            st.session_state['selected_data'] = df.iloc[start_index:end_index]
            st.write("**😎 Your auto selection has been processed**")
            # Populate the selected_mcqs_list here after auto selection is processed
            normalized_df = normalize_df(st.session_state['selected_data'], vignette_type)
            st.session_state['selected_mcqs_list'] = normalized_df['full_qa_with_qid'].tolist()

    # Conditional UI elements that should only appear after loading questions
    if st.session_state.get('manual_load_clicked') or st.session_state.get('auto_load_clicked'):
        if st.checkbox('**🖨️ Show my selected MCQs**'):
            if st.session_state.get('manual_load_clicked'):
                st.subheader("❓ Your manually selected MCQ data:")
            else:  # Assuming if not manual then it must be auto
                st.subheader("❓ Your auto selected MCQ data:")
            st.write(st.session_state['selected_data'])

        # UI for system message and prompt input
        # ATTENTION ****!!!!""""Streamlit Documentation Expert Chatbot""""!!!!**** I NEED THIS ADJUSTED TO INJECT THE PROMPTS FOUND IN from parallel_processing.prompts import v1_system_message, v1_prompt_message
 
        system_message = st.text_area("Your system message (customize to your needs):")
        prompt_message = st.text_area("Your prompt (customize to your needs):")

        # Update session state with the formatted messages
        st.session_state['formatted_system_message'] = v1_system_message,
        st.session_state['formatted_prompt'] = v1_prompt_message

        if 'batch_initiated' not in st.session_state:
            st.session_state['batch_initiated'] = False

        if 'batch_status' not in st.session_state:
            st.session_state['batch_status'] = 'Not started'

        if 'log_messages' not in st.session_state:
            st.session_state['log_messages'] = []
            
        # Check if 'Initiate batch run' button was pressed and if 'selected_mcqs_list' is not empty
        if st.button('Initiate batch run'):
            st.session_state['batch_initiated'] = True
            st.session_state['progress'] = 0

        # Check if 'selected_mcqs_list' is defined and not empty
            if 'selected_mcqs_list' in st.session_state and st.session_state['selected_mcqs_list']:
                # Add the batch run data to the queue
                batch_run_data = (
                    st.session_state['selected_mcqs_list'], 
                    st.session_state['formatted_system_message'], 
                    st.session_state['formatted_prompt']
                )                    
                batch_run_queue.put(batch_run_data)

                # Start threads to process batch runs and update the UI
                run_in_thread(process_batch_runs, batch_run_data)

                st.write("**🤓 Batch run initiated!**")
            else:
                st.error("No MCQs selected. Please select MCQs before initiating the batch run.")

    if st.session_state['batch_initiated']:
        # Display progress and logs
        col1, col2 = st.columns(2)

        with col1:
            st.write("**📊 Batch Progress:**")
            st.session_state['progress_bar'] = st.progress(st.session_state['progress'])

        with col2:
            st.write("**📜 Log Output:**")
            st.session_state['log_output'] = st.empty()
            st.session_state['log_output'].text('\n'.join(st.session_state['log_messages']))

        if st.session_state['batch_status'] == 'Completed':
            with open(output_file_path, "rb") as file:
                st.download_button(
                    label="💻 Download Results as CSV",
                    data=file,
                    file_name="batch_results.csv",
                    mime="text/csv",
                )
if __name__ == "__main__":
    main()