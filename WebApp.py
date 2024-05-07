import streamlit as st
import os
from Compare import calculate_dance_score

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
files_in_directory = os.listdir(assets_path)
st.write(f"Files in Assets directory: {files_in_directory}")

st.title("Dance Pose Analysis")

# Assuming a fixed reference video within the Assets directory
ref_video = os.path.join(assets_path, "RobotDance.mp4")

uploaded_file = st.file_uploader("Upload your dance video", type=['mp4', 'mov', 'avi'])
if uploaded_file is not None:
    temp_video_path = os.path.join(base_path, "temp_dance_video.mp4")
    with open(temp_video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())  # Save the uploaded file to disk

    # Calculate the dance score using the saved file and the reference video
    dance_score = calculate_dance_score(ref_video, temp_video_path)
    st.write(f"Dance Score: {dance_score}")
    st.video(temp_video_path)

    # Optionally, clean up by removing the temporary video file
    os.remove(temp_video_path)
