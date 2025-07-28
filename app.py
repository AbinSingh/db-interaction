import streamlit as st
import requests

API_URL = "http://localhost:8000"

def fetch_questions():
    response = requests.get(f"{API_URL}/questions")
    return response.json()

def submit_comment(qa_id, comment):
    response = requests.post(f"{API_URL}/comment/{qa_id}", json={"comment": comment})
    return response.status_code == 200

st.title("Q&A Feedback Tool")

qas = fetch_questions()

for qa in qas:
    with st.expander(f"Q: {qa['question']}"):
        st.write(f"**Prediction**: {qa['prediction']}")
        st.write(f"**Ground Truth**: {qa['ground_truth']}")
        current_comment = qa.get("comment", "")
        new_comment = st.text_area("Your Comment", value=current_comment, key=qa["id"])
        if st.button("Submit", key=f"btn_{qa['id']}"):
            if submit_comment(qa["id"], new_comment):
                st.success("Comment submitted!")
            else:
                st.error("Failed to submit comment.")
