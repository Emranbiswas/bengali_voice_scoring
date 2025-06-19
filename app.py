# import streamlit as st
# from audio_utils import transcribe_audio_file, speak_bengali_text
# from model import get_call_score_and_reason
# import os

# # Streamlit Page Config
# st.set_page_config(page_title="বাংলা কণ্ঠস্বর স্কোরিং")

# # Title
# st.title("📞 বাংলা কণ্ঠস্বর বিশ্লেষণ এবং স্কোরিং")
# # st.write("বাংলায় কথা বলুন বা একটি .wav ফাইল দিন এবং নম্রতা, কৃতজ্ঞতা ও অসভ্যতার ভিত্তিতে একটি স্কোর এবং ব্যাখ্যা পান।")

# # Upload WAV file
# uploaded_file = st.file_uploader("🔼 একটি WAV অডিও ফাইল আপলোড করুন", type=["wav"])

# if uploaded_file is not None:
#     with open("temp_audio.wav", "wb") as f:
#         f.write(uploaded_file.getbuffer())

#     st.audio("temp_audio.wav", format="audio/wav")

#     try:
#         transcription = transcribe_audio_file("temp_audio.wav", language_code="bn-BD")
#     except Exception as e:
#         st.error(f"ট্রান্সক্রিপশন ত্রুটি: {str(e)}")
#         transcription = None

#     if transcription:
#         st.success("✅ অডিও থেকে সফলভাবে লেখা তৈরি হয়েছে!")
#         st.markdown("**🗣️ ট্রান্সক্রিপ্ট:**")
#         st.write(transcription)

#         st.info("✳️ বিশ্লেষণ করা হচ্ছে...")
#         score_result = get_call_score_and_reason(transcription)

#         st.success("🔍 স্কোরিং ফলাফল:")
#         st.markdown(f"**{score_result}**")


import streamlit as st
from audio_utils import transcribe_audio_file
from model import get_call_score_and_reason
import os
from concurrent.futures import ThreadPoolExecutor

# Streamlit Page Config
st.set_page_config(page_title="বাংলা কণ্ঠস্বর স্কোরিং")
st.title("📞 বাংলা কণ্ঠস্বর বিশ্লেষণ এবং স্কোরিং")

# Upload multiple WAV files
uploaded_files = st.file_uploader("🔼 একাধিক WAV অডিও ফাইল আপলোড করুন", type=["wav"], accept_multiple_files=True)

# Worker functions
def transcribe_worker(path):
    try:
        return transcribe_audio_file(path, language_code="bn-BD")
    except Exception as e:
        st.error(f"❌ ট্রান্সক্রিপশন ত্রুটি: {str(e)}")
        return None

def score_worker(transcript):
    try:
        return get_call_score_and_reason(transcript)
    except Exception as e:
        st.error(f"❌ স্কোরিং ত্রুটি: {str(e)}")
        return None

if uploaded_files:
    # Write uploaded files to temporary disk
    temp_file_paths = []
    for idx, uploaded_file in enumerate(uploaded_files):
        temp_file_path = f"temp_audio_{idx}.wav"
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        temp_file_paths.append(temp_file_path)

    # Display audio for each file one by one
    for file_path in temp_file_paths:
        st.audio(file_path, format="audio/wav")

    # Process transcription and scoring using ThreadPoolExecutor
    with st.spinner("🔄 ট্রান্সক্রিপশন এবং স্কোর বিশ্লেষণ করা হচ্ছে..."):
        # Create a ThreadPoolExecutor to handle transcription and scoring
        with ThreadPoolExecutor(max_workers=5) as executor:
            # Transcribe all files
            transcriptions = list(executor.map(transcribe_worker, temp_file_paths))

            # Process the transcription results
            for idx, transcription in enumerate(transcriptions):
                if transcription:
                    st.success(f"✅ অডিও {idx + 1} থেকে সফলভাবে লেখা তৈরি হয়েছে!")
                    st.markdown(f"**🗣️ ট্রান্সক্রিপ্ট {idx + 1}:**")
                    st.write(transcription)

                    # Get score for the transcription
                    score_result = score_worker(transcription)

                    if score_result:
                        st.success(f"📊 স্কোরিং ফলাফল {idx + 1}:")
                        st.markdown(f"**{score_result}**")
                    else:
                        st.error(f"❌ স্কোরিং {idx + 1} ব্যর্থ হয়েছে।")
                else:
                    st.error(f"❌ অডিও {idx + 1} ট্রান্সক্রিপশন ব্যর্থ হয়েছে।")

