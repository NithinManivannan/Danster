import streamlit as st
from Compare import calculate_dance_score
import os

# Log the current working directory
st.write(f"Current Working Directory: {os.getcwd()}")

# List files in the expected directory
expected_directory = 'Assets'  # Adjust if your path is different
files_in_directory = os.listdir(expected_directory)
st.write(f"Files in {expected_directory}: {files_in_directory}")

st.title("Dance Pose Analysis")

# Upload reference video (you might want to have this pre-set or allow user to upload)
ref_video = "Assets/RobotDance.mp4"  # Assuming a fixed reference video

uploaded_file = st.file_uploader("Upload your dance video", type=['mp4', 'mov', 'avi '])
if uploaded_file is not None:
    with open("temp_dance_video.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())  # Save the uploaded file to disk

    # Calculate the dance score using the saved file and a reference video
    dance_score = calculate_dance_score(ref_video, "temp_dance_video.mp4")

    st.write(f"Dance Score: {dance_score}")
    st.video("temp_dance_video.mp4")
