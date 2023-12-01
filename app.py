import os
import json
import pandas as pd
import uuid
from dotenv import load_dotenv
from src.search_src.similarity_result import get_record_linkage
import streamlit as st

# Load environment variables from .env file
load_dotenv()

# Access the variables
mongodb_uri = os.getenv("MONGODB_URI")
artifact_store = os.getenv("ARTIFACT_STORE")
collection_name = os.getenv("COLLECTION_NAME")
chunk_file = os.getenv("CHUNK_FILE")


# open the json file
# @st.cache_data
with open(chunk_file) as f:
    chunks = json.load(f)







def display_results(target_df, result):
    """
    Display the results of the record linkage process on the Streamlit app.
    """
    if len(result) > 0:
        st.write('It seems your details below')
        st.dataframe(target_df.reset_index().drop('_id', axis= 1))
        st.write('is similar to some of our existing customers below')
        st.dataframe(result.reset_index().drop(['_id', 'details'], axis=1))
        st.markdown("### Sorry, you are not eligible for the new customer 10 days trial")
    else:
        st.markdown("### Thank you for registering. Verify your email in your inbox and start enjoying your new customer 10 days trial.")


def home():
    """
    Main function to display the Streamlit application form for user data input.
    Collects user data and checks for similarity with existing customers.
    """
     # Initialize session state variables if they don't exist
    if 'first_name' not in st.session_state:
        st.session_state['first_name'] = ''
    if 'last_name' not in st.session_state:
        st.session_state['last_name'] = ''
    if 'email' not in st.session_state:
        st.session_state['email'] = ''
    if 'phone' not in st.session_state:
        st.session_state['phone'] = ''
    if 'address' not in st.session_state:
        st.session_state['address'] = ''

    # form_key = str(uuid.uuid4())
    with st.form('form_key'):
        # Splitting the form into two columns
        col1, col2 = st.columns(2)

        with col1:
            st.session_state['first_name'] = st.text_input("First Name", value=st.session_state['first_name'])
            st.session_state['email'] = st.text_input("Email Address", value=st.session_state['email'])

        with col2:
            st.session_state['last_name'] = st.text_input("Last Name", value=st.session_state['last_name'])
            st.session_state['phone'] = st.text_input("Phone Number", value=st.session_state['phone'])
        st.session_state['address'] = st.text_input('Home Address', value=st.session_state['address'])



        # Submit button logic
        submitted = st.form_submit_button("Submit")
        if submitted:
            # Creating the full name and search term
            full_name = st.session_state['first_name'] + ' ' + st.session_state['last_name']
            email = st.session_state['email']
            address = st.session_state['address']
            phone = st.session_state['phone']
            # full_name = f'{first_name} {last_name}'.strip()
            search_term = ' '.join([full_name, email, address, phone]).lower().strip()

            # Prepare data for comparison
            customer_data = {
                'Full Name': full_name if full_name else None,
                'Email': email if email else None,
                'Address': address if address else None,
                'Phone Number': phone if phone else None,
                '_id': str(uuid.uuid4())
            }

            target_df = pd.DataFrame([customer_data]).set_index('_id')
            result = get_record_linkage(target_df, chunks, mongodb_uri, artifact_store, search_term, n=5, method='jarowinkler', threshold=0.85)

            display_results(target_df, result)
    # Place the Start Again button outside the form
    if st.button("Start Again"):
        st.session_state['first_name'] = ''
        st.session_state['last_name'] = ''
        st.session_state['email'] = ''
        st.session_state['phone'] = ''
        st.session_state['address'] = ''
        st.rerun()


if __name__ == '__main__':
    st.set_page_config(page_title="Customer Deduplication", page_icon="🧑‍🏭", layout='wide', initial_sidebar_state='expanded')
    st.title("UpSite Course Website")
    st.subheader("🔔 Welcome to UpSite Course. As a new user, register your accounts below and get 10 days free trial")
    home()
