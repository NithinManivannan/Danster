import streamlit as st
from Compare import calculate_dance_score
import os

# Determine the base path depending on the environment
if 'RENDER' in os.environ:
    base_path = '/opt/render/project/src'
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

# Define the path to the 'Assets' directory
assets_path = os.path.join(base_path, 'Assets')

# Log the current working directory and check if 'Assets' exists
st.write(f"Current Working Directory: {base_path}")
if not os.path.exists(assets_path):
    st.error("Assets directory not found. Please ensure it is included in the deployment.")
else:
    st.success(f"Assets directory is found at: {assets_path}")

# List files in the Assets directory
if os.path.exists(assets_path):
    files_in_directory = os.listdir(assets_path)
    st.write(f"Files in Assets directory: {files_in_directory}")
else:
    files_in_directory = []

st.title("Dance Pose Analysis")

# Upload reference video (adjusted to use the correct path)
ref_video = os.path.join(assets_path, "RobotDance.mp4")  # Ensure this file is in your Assets directory

uploaded_file = st.file_uploader("Upload your dance video", type=['mp4', 'mov', 'avi'])
if uploaded_file is not None:
    temp_video_path = os.path.join(base_path, "temp_dance_video.mp4")
    with open(temp_video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())  # Save the uploaded file to disk

    # Calculate the dance score using the saved file and the reference video
    if os.path.exists(ref_video):
        dance_score = calculate_dance_score(ref_video, temp_video_path)
        st.write(f"Dance Score: {dance_score}")
        st.video(temp_video_path)
    else:
        st.error("Reference video file not found. Please check your Assets directory.")

    # Optionally, clean up by removing the temporary video file
    os.remove(temp_video_path)
