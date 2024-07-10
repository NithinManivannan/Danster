import streamlit as st
from Compare import calculate_dance_score
import firebase_admin
from firebase_admin import credentials, storage

# Initialize Firebase once
def initialize_firebase():
    try:
        firebase_admin.get_app()
    except ValueError:
        cred = credentials.Certificate('danster-storage.json')
        firebase_admin.initialize_app(cred, {
            'storageBucket': 'danster-bab16.appspot.com'
        })

initialize_firebase()

st.title("Dance Pose Analysis")

robot_dance_video_url = 'https://firebasestorage.googleapis.com/v0/b/danster-bab16.appspot.com/o/RobotDance.mp4?alt=media&token=4c2cee6e-1b4a-426a-8491-b0f56e9dd26c'
st.video(robot_dance_video_url)

uploaded_file = st.file_uploader("Upload your dance video for comparison", type=['mp4', 'mov', 'avi'])
if uploaded_file is not None:
    # Upload to Firebase and get the public URL
    def upload_to_firebase(file_stream, file_name, content_type):
        bucket = storage.bucket()
        blob = bucket.blob(file_name)
        blob.upload_from_string(file_stream.read(), content_type=content_type)
        blob.make_public()
        return blob.public_url

    user_video_url = upload_to_firebase(uploaded_file, uploaded_file.name, uploaded_file.type)
    st.video(user_video_url)

    # Assume you can obtain FPS from somewhere, or use a default value
    fps = 30  # This should be dynamically obtained or set accurately if known
    dance_score, flagged_timestamps = calculate_dance_score(robot_dance_video_url, user_video_url, fps)

    st.write(f"Dance Score: {dance_score}")
    if flagged_timestamps:
        st.write("Mismatches found at the following seconds:")
        for ts in flagged_timestamps:
            st.write(f"{ts} seconds")
    else:
        st.write("No significant mismatches detected.")
